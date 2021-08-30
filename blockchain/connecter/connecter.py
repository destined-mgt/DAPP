from web3 import Web3

# 链接测试网络
from blockchain.account.addr import addr

conn = Web3(Web3.WebsocketProvider("wss://rinkeby.infura.io/ws/v3/7ecf51085fe840f49fcea75636976335"))
# 设置默认网络
conn.eth.defaultAccount = addr

# 准备私钥
with open("blockchain/account/pwd.password") as keyfile:
    encrypted_key = keyfile.read()
    private_key = conn.eth.account.decrypt(encrypted_key, "ycq5512494")
