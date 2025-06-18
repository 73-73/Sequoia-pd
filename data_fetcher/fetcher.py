# -*- encoding: UTF-8 -*-


import os
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
    data.to_csv("./data/{}/{}/{}.csv".format(period, adjust, code_name), index=False)


def fetch_stock_listing_date(code_name):
    inform = ak.stock_individual_info_em(symbol=code_name)
    return inform.iloc[8]["value"]


def fetch_all():
    all_data = ak.stock_zh_a_spot_em()
    all_data.to_csv("./data/stocks.csv", columns=["代码", "名称"], index=False)
    subset = all_data[["代码", "名称"]]
    stocks = [tuple(x) for x in subset.values]
    for adjust in ["qfq", "hfq", "raw"]:
        for period in ["daily", "monthly", "weekly"]:
            os.makedirs("./data/{}/{}".format(period, adjust), exist_ok=True)
            for stock in stocks:
                date = fetch_stock_listing_date(stock[0])
                fetch_stock_data(stock[0], period, date, adjust)


if __name__ == "__main__":
    fetch_all()
