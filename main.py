import pandas as pd
import numpy as np
import datetime
import math
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from sklearn import preprocessing
from class import *
from functions import *

##数据准备与预处理##====
data = pd.read_csv(r"C:\Users\Desktop\data.csv",index_col=0)
data.index = pd.to_datetime(data.index)
data['tradeday'] = data.index.date
data['time'] = data.index.time
# 获取交易日序列
date1=data[['tradeday']].drop_duplicates()

##一次开仓##====
for i in range(len(date1)):
    print("开始处理日期" + str(date1.tradeday[i]) + "的数据")
    current_data = data[data['tradeday']==date1.tradeday[i]]
    length = len(current_data)
    print("当前日期有" + str(length) + "条数据")

    # 早晨样本观察开始索引--9:16
    morning_sample_start = 0

    # 早晨样本观察结束索引 --10:06
    morning_sample_end = 50

    # 早晨平仓索引 --11:30
    morning_position_close = 134

    # 下午样本观察开始索引  --11:12
    afternoon_sample_start = 116

    # 下午样本观察结束索引  --13:32
    afternoon_sample_end = 166

    # 下午平仓索引
    afternoon_position_close = length

    # 一次开仓
    print("----------------------------------------")
    print("一次开仓，开始处理......")
    calculate_transaction_data(Configuration.uni_transaction_data, date1.tradeday[i], current_data,
                                                 morning_sample_start, morning_sample_end, afternoon_position_close)

    print("\r\n")

    
  
  #策略评价：
#样本内 2010.4.16 - 2012.12.31
for i in range(len(date1_sample_in)):
    print("开始处理日期" + str(date1_sample_in.tradeday[i]) + "的数据")
    current_data = data[data['tradeday']==date1_sample_in.tradeday[i]]
    length = len(current_data)
    print("当前日期有" + str(length) + "条数据")

    # 早晨样本观察开始索引
    morning_sample_start = 0

    # 早晨样本观察结束索引
    morning_sample_end = 50

    # 早晨平仓索引
    morning_position_close = 134

    # 下午样本观察开始索引
    afternoon_sample_start = 114

    # 下午样本观察结束索引
    afternoon_sample_end = 164

    # 下午平仓索引
    afternoon_position_close = length

    # 一次开仓
    print("----------------------------------------")
    print("一次开仓，开始处理......")
    calculate_transaction_data(Configuration.uni_transaction_data, date1_sample_in.tradeday[i], current_data,
                                                 morning_sample_start, morning_sample_end, afternoon_position_close)

    print("\r\n")

#样本外 2013.01.01 - 2015.01.30
for i in range(len(date1_sample_out)):
    print("开始处理日期" + str(date1_sample_out.tradeday[i]) + "的数据")
    current_data = data[data['tradeday']==date1_sample_out.tradeday[i]]
    length = len(current_data)
    print("当前日期有" + str(length) + "条数据")

    # 早晨样本观察开始索引
    morning_sample_start = 0

    # 早晨样本观察结束索引
    morning_sample_end = 50

    # 早晨平仓索引
    morning_position_close = 134

    # 下午样本观察开始索引
    afternoon_sample_start = 114

    # 下午样本观察结束索引
    afternoon_sample_end = 164

    # 下午平仓索引
    afternoon_position_close = length

    # 一次开仓
    print("----------------------------------------")
    print("一次开仓，开始处理......")
    calculate_transaction_data(Configuration.uni_transaction_data, date1_sample_out.tradeday[i], current_data,
                                                 morning_sample_start, morning_sample_end, afternoon_position_close)

    print("\r\n")

##多次开仓##====
"""
    多次开仓的交易策略中，上午开仓同原始策略一致，观察开盘后50分钟的收盘价样本，随后决定是否开仓。
    但是在11：30上午收市时平仓。下午开盘则充分利用上午的数据，观察包括上午收盘数据在内11:12至13:32的数据样本，
    并在13:33决定下午是否开仓。
"""
for i in range(len(date1)):
    print("开始处理日期" + str(date1.tradeday[i]) + "的数据")
    current_data = data[data['tradeday']==date1.tradeday[i]]
    length = len(current_data)
    print("当前日期有" + str(length) + "条数据")

    # 早晨样本观察开始索引
    morning_sample_start = 0

    # 早晨样本观察结束索引
    morning_sample_end = 50

    # 早晨平仓索引
    morning_position_close = 134

    # 下午样本观察开始索引 -- 11:12
    afternoon_sample_start = 116

    # 下午样本观察结束索引 --13:32
    afternoon_sample_end = 166

    # 下午平仓索引
    afternoon_position_close = length

    # 多次开仓 --> 早晨开仓
    print("----------------------------------------")
    print("多次开仓 --> 早晨开仓，开始处理......")
    calculate_transaction_data(Configuration.multi_transaction_data, date1.tradeday[i], current_data,
                               morning_sample_start,
                               morning_sample_end, morning_position_close + 1)
    # 多次开仓 --> 下午开仓
    print("----------------------------------------")
    print("多次开仓 --> 下午开仓，开始处理......")
    calculate_transaction_data(Configuration.multi_transaction_data, date1.tradeday[i], current_data,
                               afternoon_sample_start,
                               afternoon_sample_end, afternoon_position_close)


    print("\r\n")




