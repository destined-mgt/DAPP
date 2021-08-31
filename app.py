from flask import Flask

from blockchain.scheduler.scheduler import Switch

# 初始化日志系统(DEBUG等级)
from utility.Log import SetLevel

SetLevel("DEBUG")

_, loop = Switch(0, "init")
loop.start()

app = Flask(__name__)

if __name__ == '__main__':
    app.run()
