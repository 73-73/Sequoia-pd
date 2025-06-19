# -*- encoding: UTF-8 -*-


import csv
import os
import threading
import time
import akshare as ak
from concurrent.futures import ThreadPoolExecutor, as_completed


from time_out_decorator import timeout


def fetch_stock_data(code_name, period, adjust):
    get_stock_data = False
    printed = False
    date = None
    while get_stock_data == False:
        try:
            get_stock_data, date = fetch_stock_listing_date(code_name)
        except Exception as e:
            if printed == False:
                print("refetch ./data/{}/{}/{}.csv".format(period, adjust, code_name))
                printed = True
    adj = adjust
    if adj == "raw":
        adj = ""
    get_stock_data = False
    while get_stock_data == False:
        try:
            data = ak.stock_zh_a_hist(
                symbol=code_name,
                period=period,
                start_date=date,
                end_date="20250618",
                adjust=adj,
            )
            data.to_csv(
                "./data/{}/{}/{}.csv".format(period, adjust, code_name),
                index=False,
            )
            get_stock_data = True

        except Exception as e:
            time.sleep(0.1)
            if printed == False:
                print("refetch ./data/{}/{}/{}.csv".format(period, adjust, code_name))
                printed = True

    print("get ./data/{}/{}/{}.csv".format(period, adjust, code_name))


def fetch_stock_listing_date(code_name):
    inform = ak.stock_individual_info_em(symbol=code_name)
    return True, inform.iloc[8]["value"]


# @timeout(30)
def fetch_all(stop_event=None):
    stocks = []
    with open(
        "./data/stocks.csv",
        mode="r",
        encoding="utf-8",
    ) as file:
        reader = csv.reader(file)
        next(reader)  # 跳过第一行（标题行）
        stocks = [row for row in reader]  # 读取剩余行
    tasks = []
    for adjust in ["qfq", "hfq", "raw"]:
        for period in ["daily", "monthly", "weekly"]:
            os.makedirs(f"./data/{period}/{adjust}", exist_ok=True)
            for code in stocks:
                file_path = f"./data/{period}/{adjust}/{code[0]}.csv"
                if not os.path.exists(file_path):  # 只添加未下载的任务
                    tasks.append((code[0], period, adjust))
    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有任务
        futures = [executor.submit(fetch_stock_data, *task) for task in tasks]

        try:
            # 等待所有任务完成
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"任务失败: {str(e)}")

            print("所有文件下载完成！")
        except KeyboardInterrupt:
            print("\n收到中断信号，正在停止...")
            stop_event.set()
            # 取消未完成的任务
            for future in futures:
                future.cancel()
            raise

    print("fetch successfully")


if __name__ == "__main__":
    stop_event = threading.Event()
    fetch_all(stop_event)
# while True:
#     time.sleep(2)
