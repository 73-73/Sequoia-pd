# -*- encoding: UTF-8 -*-


import csv
import os
import time
import akshare as ak


def fetch_stock_data(code_name, period, start_date, adjust):
    adj = adjust
    if adj == "raw":
        adj = ""
    data = ak.stock_zh_a_hist(
        symbol=code_name,
        period=period,
        start_date=start_date,
        end_date="20250618",
        adjust=adj,
    )
    data.to_csv(
        "/home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
            period, adjust, code_name
        ),
        index=False,
    )
    return True


def fetch_stock_listing_date(code_name):
    inform = ak.stock_individual_info_em(symbol=code_name)
    return True, inform.iloc[8]["value"]


def fetch_all():

    stocks = []
    with open(
        "/home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/stocks.csv",
        mode="r",
        encoding="utf-8",
    ) as file:
        reader = csv.reader(file)
        next(reader)  # 跳过第一行（标题行）
        stocks = [row for row in reader]  # 读取剩余行

    # 使用示例
    for adjust in ["qfq", "hfq", "raw"]:
        for period in ["daily", "monthly", "weekly"]:
            os.makedirs(
                "/home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}".format(
                    period, adjust
                ),
                exist_ok=True,
            )
            for stock in stocks:
                if (
                    os.path.exists(
                        "/home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
                            period, adjust, stock[0]
                        )
                    )
                    == True
                ):
                    print(
                        "skip /home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
                            period, adjust, stock[0]
                        )
                    )
                    continue

                get_stock_data = False
                printed = False
                while get_stock_data == False:
                    try:
                        get_stock_data, date = fetch_stock_listing_date(stock[0])
                    except Exception as e:
                        time.sleep(1)
                        if printed == False:
                            print(
                                "refetch /home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
                                    period, adjust, stock[0]
                                )
                            )
                            printed = True
                get_stock_data = False
                printed = False
                while get_stock_data == False:
                    try:
                        get_stock_data = fetch_stock_data(
                            stock[0], period, date, adjust
                        )
                    except Exception as e:
                        time.sleep(1)
                        if printed == False:
                            print(
                                "refetch /home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
                                    period, adjust, stock[0]
                                )
                            )
                            printed = True
                print(
                    "get /home/yucheb/code/python/Sequoai-Cheb/data_fetcher/data/{}/{}/{}.csv".format(
                        period, adjust, stock[0]
                    )
                )
                # time.sleep(10)


if __name__ == "__main__":
    fetch_all()
