from flask import Flask

from blockchain.scheduler.scheduler import Switch

_, loop = Switch(0, "init")
loop.start()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
