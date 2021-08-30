import sys
import threading
import time

# 监听设置阶段事件
from web3 import Web3

from blockchain.contract.work.conn_work import contract
from blockchain.contract.work.function.func_GetModelToVerify import GetModelToVerify
from blockchain.contract.work.function.func_GetModelsToMerge import GetModelToMerge
from blockchain.contract.work.function.func_Merge import Merge
from blockchain.contract.work.function.func_NextStep import NextStep
from blockchain.contract.work.function.func_SubmitModel import SubmitModel
from blockchain.contract.work.function.func_Verify import Verify
from interface.MergeModels import MergeModels
from interface.Score import Score

flter_reward = contract.events.reward.createFilter(fromBlock="latest")
# 监听结束设置阶段事件
flter_submitModel = contract.events.submitModel.createFilter(fromBlock="latest")
# 监听选举阶段事件
flter_verifyModel = contract.events.verifyModel.createFilter(fromBlock="latest")
# 监听结束选举阶段事件
flter_mergeModel = contract.events.mergeModel.createFilter(fromBlock="latest")
# 模型分数
flter_modelscore = contract.events.modelscore.createFilter(fromBlock="latest")
# 最终模型
flter_finalscore = contract.events.finalscore.createFilter(fromBlock="latest")

mag = Web3.toChecksumAddress("0x27e8Efa6d4522a5fc177C1947Cc82A99Ca7445a1")


def WorkLoop(work_status=10):
    sbumitModelTime = 10
    startSubmitModelTime = 0
    verifyModelTime = 1
    startVerifyModelTime = 0
    mergeModelTime = 5
    startMergeModelTime = 0
    while True:
        event_reward = flter_reward.get_new_entries()
        event_submitModel = flter_submitModel.get_new_entries()
        event_verifyModel = flter_verifyModel.get_new_entries()
        event_mergeModel = flter_mergeModel.get_new_entries()
        event_modelscore = flter_modelscore.get_new_entries()
        event_finalscore = flter_finalscore.get_new_entries()

        if work_status == 10:
            result = NextStep(mag)
            if result['error'] is None:
                work_status = result['status']
        elif work_status == 11:
            # 模型提交阶段，推动该阶段结束
            model = "0x7465737400000000000000000000000000000000000000000000000000000001"
            SubmitModel(mag, model)
            localTime = time.time()
            if localTime - startSubmitModelTime > sbumitModelTime:
                result = NextStep(mag)
                if result['error'] is None:
                    work_status = result['status']
            else:
                print("waiting to submit:", sbumitModelTime - (localTime - startSubmitModelTime))
        elif work_status == 12:
            # 模型提交阶段结束，推动进入模型验证阶段
            result = NextStep(mag)
            if result['error'] is None:
                work_status = result['status']
        elif work_status == 13:
            # 模型验证阶段，推动该阶段结束
            # 验证模型
            # 获取模型
            result = GetModelToVerify(mag)
            model = result['model']
            if model:
                # TODO:swarmID=>file
                # 模型打分(暴露)
                sc = Score(model)
                # 模型上传
                Verify(mag, sc)
            localTime = time.time()
            if localTime - startVerifyModelTime > verifyModelTime:
                result = NextStep(mag)
                if result['error'] is None:
                    work_status = result['status']
        elif work_status == 14:
            # 推动进入模型合并阶段
            result = NextStep(mag)
            if result['error'] is None:
                work_status = result['status']
        elif work_status == 15:
            # 推动模型合并阶段
            result = GetModelToMerge(mag)
            models = result['models']
            if models:
                # TODO:swarmIDs=>files
                # 模型合并(暴露)
                model = MergeModels(mag, models)
                # 模型上传
                Merge(mag, model)
            localTime = time.time()
            if localTime - startMergeModelTime > mergeModelTime:
                result = NextStep(mag)
                if result['error'] is None:
                    work_status = result['status']
        # -----------------------------------------------------------------------------------------------------------------------
        if event_submitModel:
            work_status = max(11, work_status)
            startSubmitModelTime = event_submitModel[0]['args']['startTime']
            print(startSubmitModelTime)
            # 提交模型
            model = "0x7465737400000000000000000000000000000000000000000000000000000001"
            SubmitModel(mag, model)
        if event_verifyModel:
            work_status = max(13, work_status)
            startVerifyModelTime = event_verifyModel[0]['args']['startTime']
            # 获取模型
            result = GetModelToVerify(mag)
            model = result['model']
            if model:
                # TODO:swarmID=>file
                # 模型打分(暴露)
                sc = Score( model)
                # 模型上传
                Verify(mag, sc)
                print("model", model, " score:", sc)
        if event_mergeModel:
            work_status = max(15, work_status)
            startMergeModelTime = event_mergeModel[0]['args']['startTime']
            # 获取模型数组
            result = GetModelToMerge(mag)
            models = result['models']
            if models:
                # TODO:swarmIDs=>files
                # 模型合并(暴露)
                model = MergeModels(models)
                # 模型上传
                Merge(mag, model)
        if event_modelscore:
            print("****result-model****:", event_modelscore[0]['args']['model'], "score:",
                  event_modelscore[0]['args']['score'])
        if event_finalscore:
            print("****final-model****:", event_finalscore[0]['args']['model'], "score:",
                  event_finalscore[0]['args']['score'])
            work_status = 16
        print("current status:", work_status)
        from blockchain.scheduler.scheduler import Switch
        needSwtich, loop = Switch(work_status, "work")
        if needSwtich:
            loop.start()
            break


listen_thread_Work = threading.Thread(target=WorkLoop)
