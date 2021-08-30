from flask import Flask

from blockchain.scheduler.scheduler import Switch

# 初始化日志系统(DEBUG等级)
from utility import Log
from utility.Log import SetLevel
from utility.ParseConfig import GetConfig

SetLevel("DEBUG")
# 系统设置参数文件解析
cfg = GetConfig("./config", "blockchain")
bc_pwd_file = cfg[0][1]
bc_websocket_provider = cfg[1][1]
bc_interface_addr = cfg[2][1]

Log.logger.info("bc_pwd_file=%s \n"
                "bc_websocket_provide=%s\n"
                "bc_interface_addr=%s" % (bc_pwd_file, bc_websocket_provider, bc_interface_addr))
Log.logger.info("start the decentralization process....")
_, loop = Switch(0, "init")
loop.start()

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
