import sys
import threading
import time

from web3 import Web3

from blockchain.contract.workArg.conn_workArg import contract
from blockchain.contract.workArg.function.func_DecideC import DecideC
from blockchain.contract.workArg.function.func_NextStep import NextStep
from utility import Log

flter_reward = contract.events.reward.createFilter(fromBlock="latest")
flter_decideC = contract.events.decideC.createFilter(fromBlock="latest")
flter_finalC = contract.events.finalC.createFilter(fromBlock="latest")

acc = 0
mag = Web3.toChecksumAddress("0x27e8Efa6d4522a5fc177C1947Cc82A99Ca7445a1")


def WorkArgLoop(workArg_status=8):
    global acc
    startDecideCTime = 0
    decideCTime = 5
    while True:
        event_reward = flter_reward.get_new_entries()
        event_decideC = flter_decideC.get_new_entries()
        event_finalC = flter_finalC.get_new_entries()
        if workArg_status == 8:
            result = NextStep(mag)
            if result['error'] is None:
                workArg_status = result['status']
        elif workArg_status == 9:
            # 准确率提交阶段，推动该阶段结束
            DecideC(mag, 60)
            localTime = time.time()
            if localTime - startDecideCTime > decideCTime:
                result = NextStep(mag)
                if result['error'] is None:
                    workArg_status = result['status']
        # -----------------------------------------------------------------------------------------------------------------------
        if event_decideC:
            workArg_status = max(9, workArg_status)
            startDecideCTime = event_decideC[0]['args']['startTime']
            # 提交一次
            DecideC(mag, 60)
        if event_finalC:
            workArg_status = max(10, workArg_status)
            acc = event_finalC[0]['args']['c']
            Log.logger.info("****acc****:%s" % str(acc))
        # 每当接受该指令，线程关闭，引导下一线程启动
        Log.logger.info("current status:%s" % str(workArg_status))
        from blockchain.scheduler.scheduler import Switch
        needSwtich, loop = Switch(workArg_status, "workArg")
        if needSwtich:
            loop.start()
            break

    listen_thread_WorkArg = threading.Thread(target=WorkArgLoop)
