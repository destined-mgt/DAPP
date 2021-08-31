import sys
import threading
import time

from web3 import Web3

from blockchain.contract.elect.conn_elect import contract
from blockchain.contract.elect.function.func_Close import Close
from blockchain.contract.elect.function.func_DecideTime import DecideTime
from blockchain.contract.elect.function.func_Elect import Elect
from blockchain.contract.elect.function.func_NextStep import NextStep
from utility import Log
from utility.ParseConfig import GetConfig

flter_reward = contract.events.reward.createFilter(fromBlock="latest")
flter_startSetting = contract.events.startSetting.createFilter(fromBlock="latest")
flter_endSetting = contract.events.endSetting.createFilter(fromBlock="latest")
flter_startElect = contract.events.startElect.createFilter(fromBlock="latest")
flter_endElect = contract.events.endElect.createFilter(fromBlock="latest")
flter_reply = contract.events.reply.createFilter(fromBlock="latest")
flter_newLoop = contract.events.newLoop.createFilter(fromBlock="latest")
flter_work = contract.events.work.createFilter(fromBlock="latest")

mag = Web3.toChecksumAddress("0x27e8Efa6d4522a5fc177C1947Cc82A99Ca7445a1")


def ElectLoop(elect_status=0):
    settingStartTime = 0
    settingTime = 5
    electStartTime = 0
    electTime = 5
    replyStartTime = 0
    replyTime = 5
    while True:
        event_reward = flter_reward.get_new_entries()
        event_startSetting = flter_startSetting.get_new_entries()
        event_endSetting = flter_endSetting.get_new_entries()
        event_startElect = flter_startElect.get_new_entries()
        event_endElect = flter_endElect.get_new_entries()
        event_reply = flter_reply.get_new_entries()
        event_newLoop = flter_newLoop.get_new_entries()
        event_work = flter_work.get_new_entries()
        if elect_status == 0:
            result = NextStep(mag)
            if result['error'] is None:
                elect_status = result['status']
        elif elect_status == 1:
            cfg = GetConfig("config")
            decide_time = cfg.getint("DAPP", "elect_decide_time")
            # 读取配置文件
            DecideTime(mag, decide_time)
            localTime = time.time()
            if localTime - settingStartTime > settingTime:
                result = NextStep(mag)
                if result['error'] is None:
                    elect_status = result['status']
        elif elect_status == 2:
            result = NextStep(mag)
            if result['error'] is None:
                elect_status = result['status']
        elif elect_status == 3:
            cfg = GetConfig("config")
            is_need_join_elect = cfg.getboolean("DAPP", "is_need_join_elect")
            # 读取配置文件
            if is_need_join_elect:
                elect_pledge_eth = cfg.getint("DAPP", "elect_pledge_eth")
                Elect(mag, elect_pledge_eth)
            localTime = time.time()
            if localTime - electStartTime > electTime:
                result = NextStep(mag)
                if result['error'] is None:
                    elect_status = result['status']
        elif elect_status == 16:
            Log.logger.info("***loop end***")
            cfg = GetConfig("config")
            is_need_next_loot = cfg.getboolean("DAPP", "is_need_next_loot")
            # 读取配置文件，获取是否进行下一轮的数据
            if is_need_next_loot:
                result = NextStep(mag)
            if result['error'] is None:
                elect_status = result['status']
        elif elect_status == 17:
            Close(mag)
            localTime = time.time()
            if localTime - replyStartTime > replyTime:
                result = NextStep(mag)
                if result['error'] is None:
                    elect_status = result['status']
        # -----------------------------------------------------------------------------------------------------------------------
        if event_startSetting:
            elect_status = max(1, elect_status)
            settingStartTime = event_startSetting[0]['args']['startTime']
            # 提交一次
            cfg = GetConfig("config")
            decide_time = cfg.getint("DAPP", "elect_decide_time")
            # 读取配置文件
            DecideTime(mag, decide_time)
        if event_endSetting:
            elect_status = max(2, elect_status)
            finalTime = event_endSetting[0]['args']['finalTime']
            Log.logger.info("****elect time****:%s" % str(finalTime))
        if event_startElect:
            elect_status = max(3, elect_status)
            electStartTime = event_startElect[0]['args']['startTime']
            cfg = GetConfig("config")
            is_need_join_elect = cfg.getboolean("DAPP", "is_need_join_elect")
            # 读取配置文件
            if is_need_join_elect:
                elect_pledge_eth = cfg.getint("DAPP", "elect_pledge_eth")
                Elect(mag, elect_pledge_eth)
        if event_endElect:
            elect_status = max(4, elect_status)
            committees = event_endElect[0]['args']['committees']
            Log.logger.info("****committees****:%s" % str(committees))
        if event_work:
            elect_status = max(16, elect_status)
        if event_reply:
            elect_status = max(17, elect_status)
            replyStartTime = event_reply[0]['args']['startTime']
        if event_newLoop:
            elect_status = 0
            Log.logger.info("****start loop****")

        Log.logger.info("current status:%s" % str(elect_status))
        from blockchain.scheduler.scheduler import Switch
        needSwtich, loop = Switch(elect_status, "elect")
        if needSwtich:
            loop.start()
            break
