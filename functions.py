#计算情绪平稳度
def calculate_emotional_stability(data):
    length_of_data = len(data)

    max_sum = 0.0  # 最大回撤求和
    min_sum = 0.0  # 反向最大回撤求和
    for i in range(0, length_of_data):
        close_i = data.close[i]
        max_value = 0.0  # 计算一分钟的最大回撤
        min_value = 0.0  # 计算一分钟的反向最大回撤
        for j in range(i + 1, length_of_data):
            close_j = data.close[j]

            calculate_result = 1 - close_j / close_i

            if calculate_result > max_value:
                max_value = calculate_result

            if calculate_result < min_value:
                min_value = calculate_result

        max_sum += max_value  # 把每一分钟的最大回撤相加
        min_sum += -min_value  # 把每一分钟的反向最大回撤相加（注意取负值）

    max_ave = max_sum / length_of_data  # 平均最大回撤
    min_ave = min_sum / length_of_data  # 平均最大反向回撤

    print("平均最大回撤：" + str(max_ave))
    print("平均最大反向回撤：" + str(min_ave))

    # 比较平均最大回撤和平均最大反向回撤，返回小的
    if max_ave <= min_ave:
        print("采用平均最大回撤作为平稳度")
        return max_ave
    else:
        print("采用平均最大反向回撤作为平稳度")
        return min_ave

      
 #计算交易数据
def calculate_transaction_data(transaction_data, date_value, date_init_list, sample_observation_begin_index,
                                   sample_observation_end_index, finish_index):
        # 根据样本观察索引区间获取样本数据
    sample_observation = date_init_list[sample_observation_begin_index:sample_observation_end_index]
        # sample_observation = current_data[114:164]

    # print("样本长度为：" + str(len(sample_observation)))

        # 根据样本数据计算情绪平稳度
    emotional_stability = calculate_emotional_stability(sample_observation)

        # 情绪平稳度小于阈值，决定开仓
    if emotional_stability < Configuration.emotional_stability_threshold:
        print("情绪平稳度小于阈值，选择开仓")

            # 样本观察收盘价
        sample_observation_end_close = date_init_list.close[sample_observation_end_index - 1]

            # 样本观察开盘价
        sample_observation_begin_open = date_init_list.open[sample_observation_begin_index]

            # 在样本观察之后的下一分钟开盘买入
        buy_price = date_init_list.open[sample_observation_end_index]

            # 如果样本观察的收盘价大于样本观察开盘价，则做多
        if sample_observation_end_close > sample_observation_begin_open:
            print("开始做多")
            long = 1
        else:
            print("开始做空")
            long = 0

        for i_value in range(sample_observation_end_index + 1, finish_index):

                # 在开盘之后判断是否需要止损
            sell_price = date_init_list.open[i_value]

                # 如果做多，则用卖出价格减去买入价格
            if long == 1:
                percent = (sell_price - buy_price) / buy_price

                # 如果做空，则用买入价格减去卖出价格
            else:
                percent = (buy_price - sell_price) / sell_price

                # 如果损失大于止损阈值，则平仓止损
            if percent < 0 and abs(percent) > Configuration.stop_loss_threshold:
                print("平仓止损")

                transaction_data["money"] = transaction_data["money"] * (1 + percent - Configuration.service_charge)
                transaction_data["details"].append(
                        dict(date=date_value, emotion = emotional_stability, money=transaction_data["money"],
                             transaction = 1, direction = long, duration = i_value - sample_observation_end_index, pct = percent))
                return

        print("收盘平仓")
        sell_price = date_init_list.close[finish_index - 1]

            # 如果做多，则用卖出价格减去买入价格
        if long == 1:
            percent = (sell_price - buy_price) / buy_price

            # 如果做空，则用买入价格减去卖出价格
        else:
            percent = (buy_price - sell_price) / sell_price

        transaction_data["money"] = transaction_data["money"] * (1 + percent - Configuration.service_charge)
        transaction_data["details"].append(
                dict(date=date_value, emotion = emotional_stability, money=transaction_data["money"],
                     transaction = 1, direction = long, duration = finish_index-sample_observation_end_index, pct = percent))
        return

    else:
        print("情绪平稳度大于阈值，选择不开仓")
        transaction_data["details"].append(dict(date=date_value, emotion = emotional_stability,
                                                money=transaction_data["money"],transaction = 0,direction = -1,
                                                duration = 0, pct = 0))
        return

    

# 从交易数据中获取绘制折线图所需要的数据
def get_line_chart_data(transaction_data):
    # 保存x轴的数据 日期
    date_list = []

    # 保存y轴的数据 累计收益
    money_list = []
    value_list = []

    #保存情绪稳定度数据
    # emotional_stability_list = []
    # #保存是否开仓、做多做空、交易所时间、涨跌幅数据
    # transaction_list = []
    # direction_list = []
    # duration_list = []
    # pct_list = []


    for details in transaction_data["details"]:
        date_value = details["date"]
        money_value = details["money"]
        # emotional_value = details["emotion"]
        # transaction_value = details["transaction"]
        # direction_value = details["direction"]
        # duration_value = details["duration"]
        # pct_value = details["pct"]

        date_list.append(date_value)

        money_list.append(money_value - Configuration.init_money)
        value_list.append(money_value)
        # emotional_stability_list.append(emotional_value)
        # transaction_list.append(transaction_value)
        # direction_list.append(direction_value)
        # duration_list.append(duration_value)
        # pct_list.append(pct_value)

    return dict(date_list=date_list, money_list=money_list,value_list = value_list)
                # emotional_stability_list=emotional_stability_list,
                # transaction_list = transaction_list,
                # direction_list = direction_list, duration_list=duration_list,pct_list=pct_list)



