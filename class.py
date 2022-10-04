class Configuration:

    # 情绪平稳度阈值
    emotional_stability_threshold = 9/ 10000.0   #根据需要进行修改

    # 止损阈值
    stop_loss_threshold = 0.5 / 100.0

    # 初始金额
    # 设置为100是因为算到最后的结果刚好可以以百分比表示
    init_money = 100

    # 多次开仓交易的数据
    # money保存的是交易当前的金额
    # details保存的是所有的交易数据
    multi_transaction_data = dict(money=init_money, details=[])

    # 一次开仓交易的数据
    # money保存的是交易当前的金额
    # details保存的是所有的交易数据
    uni_transaction_data = dict(money=init_money, details=[])

    # 交易成本(双边)
    # 在计算收益的时候需要去掉
    service_charge = 2 / 10000.0
