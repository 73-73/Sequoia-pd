# -*- encoding: UTF-8 -*-

import utils
from talib import ATR
import strategy.enter as enter
import strategy.low_atr as low_atr
import strategy.enter as enter
import logging

# data = utils.load("000012.h5")
#
# rolling_window = 21
# moving_average = 20
#
# average_true_range_list = ATR(
#     data.high.values[-rolling_window:],
#     data.low.values[-rolling_window:],
#     data.close.values[-rolling_window:],
#     timeperiod=moving_average
# )
#
# average_true_range = average_true_range_list[-1]
#
# stock = "000977"
# name = "浪潮信息"
# data = utils.read_data(stock)
# # print(data)
# result = enter.check_ma(stock, data)
# logging.info("low atr check {0}'s result: {1}".format(stock, result))
#
# rolling_window = 21
# moving_average = 20
#
# average_true_range = ATR(
#         data.high.values[-rolling_window:],
#         data.low.values[-rolling_window:],
#         data.close.values[-rolling_window:],
#         timeperiod=moving_average
#     )
# print(data['high'].values)
#
# print(average_true_range)

# print(atr_list)
# atr = atr_list[-1]
# print(atr)
# print(enter.check_volume(stock, data, end_date="2018-01-02"))
# import notify
#
# results = ['300188', '600271']
# msg = '\n'.join("*代码：%s" % ''.join(x) for x in results)
# notify.notify(msg)
# print(results)

# import tushare as ts
#
# data = ts.get_stock_basics()
# print(data)

import db

t_shelve = db.ShelvePersistence()
t_shelve.positions()