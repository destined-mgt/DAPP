import threading
import time

from blockchain.account.addr import addr
from blockchain.contract.transer.conn_transer import contract

# 监听ToWhom事件
flter_ToWhom = contract.events.ToWhom.createFilter(fromBlock="latest")


def ListenToWhom():
    poll_interval = 10
    while True:
        new_event = flter_ToWhom.get_new_entries()
        if new_event and new_event[0]['args']['who'] == addr:
            fileID = new_event[0]['args']['fileID']
            print("recived file :", fileID)
            # 准备接收文件
            from blockchain.contract.transer.function.func_ReciveFile import ReciveFile
            json_data = ReciveFile(fileID)
            swarm_id = json_data['swarmId']
            print("file id (", fileID, ")", " -> ", "swarm id (", swarm_id, ")")
        time.sleep(poll_interval)


listen_thread_ToWhom = threading.Thread(target=ListenToWhom)
