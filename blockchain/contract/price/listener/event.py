import sys
import threading
import time

from web3 import Web3

from blockchain.contract.price.conn_price import contract
from blockchain.contract.price.function.func_Buy import Buy
from blockchain.contract.price.function.func_DecidePrice import DecidePrice
from blockchain.contract.price.function.func_NextStep import NextStep
from utility import Log
from utility.ParseConfig import GetConfig

flter_reward = contract.events.reward.createFilter(fromBlock="latest")
flter_decidePrice = contract.events.decidePrice.createFilter(fromBlock="latest")
flter_finalPrice = contract.events.finalPrice.createFilter(fromBlock="latest")
flter_buyModel = contract.events.buyModel.createFilter(fromBlock="latest")

price = -1
mag = Web3.toChecksumAddress("0x27e8Efa6d4522a5fc177C1947Cc82A99Ca7445a1")


def PriceLoop(Price_status=4):
    global price
    startDecidePriceTime = 0
    decidePriceTime = 5
    startBuyTime = 0
    buyTime = 5
    while True:
        event_reward = flter_reward.get_new_entries()
        event_decidePrice = flter_decidePrice.get_new_entries()
        event_finalPrice = flter_finalPrice.get_new_entries()
        event_buyModel = flter_buyModel.get_new_entries()
        if Price_status == 4:
            result = NextStep(mag)
            if result['error'] is None:
                Price_status = result['status']
        elif Price_status == 5:
            cfg = GetConfig("config")
            decide_price = cfg.getint("DAPP", "decide_price")
            # 读取配置文件
            DecidePrice(mag, decide_price)
            localTime = time.time()
            if localTime - startDecidePriceTime > decidePriceTime:
                result = NextStep(mag)
                if result['error'] is None:
                    Price_status = result['status']
        elif Price_status == 6:
            result = NextStep(mag)
            if result['error'] is None:
                Price_status = result['status']
        elif Price_status == 7:
            cfg = GetConfig("config")
            is_need_buy = cfg.getboolean("DAPP", "is_need_buy")
            # 读取配置文件
            if price >= 0 and is_need_buy:
                Buy(mag, price)
            localTime = time.time()
            if localTime - startBuyTime > buyTime:
                result = NextStep(mag)
                if result['error'] is None:
                    Price_status = result['status']
        # -----------------------------------------------------------------------------------------------------------------------
        if event_decidePrice:
            Price_status = max(5, Price_status)
            startDecidePriceTime = event_decidePrice[0]['args']['startTime']
            # 提交一次
            cfg = GetConfig("config")
            decide_price = cfg.getint("DAPP", "decide_price")
            # 读取配置文件
            DecidePrice(mag, decide_price)
        if event_finalPrice:
            Price_status = max(6, Price_status)
            price = event_finalPrice[0]['args']['price']
            Log.logger.info("****final price****:%s" % str(price))

        if event_buyModel:
            Price_status = max(7, Price_status)
            startBuyTime = event_buyModel[0]['args']['startTime']
            price = event_buyModel[0]['args']['price']
            # 读取参数是否购买模型
            cfg = GetConfig("config")
            is_need_buy = cfg.getboolean("DAPP", "is_need_buy")
            # 读取配置文件
            if price >= 0 and is_need_buy:
                Buy(mag, price)

        Log.logger.info("current status:%s" % str(Price_status))
        from blockchain.scheduler.scheduler import Switch
        needSwtich, loop = Switch(Price_status, "price")
        if needSwtich:
            loop.start()
            break


listen_thread_Price = threading.Thread(target=PriceLoop)
