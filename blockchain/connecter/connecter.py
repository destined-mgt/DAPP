from web3 import Web3

# 链接测试网络
from blockchain.account.addr import addr
from utility.ParseConfig import GetConfig

cfg = GetConfig("config")
bc_websocket_provider = cfg.get("SYSTEM", "bc_websocket_provider")
bc_interface_addr = cfg.get("SYSTEM", "bc_interface_addr")
bc_pwd_file = cfg.get("SYSTEM", "bc_pwd_file")
bc_pwd_file_pwd = cfg.get("SYSTEM", "bc_pwd_file_pwd")

conn = Web3(Web3.WebsocketProvider(bc_websocket_provider))
# 设置默认网络
conn.eth.defaultAccount = addr
# 准备私钥
with open(bc_pwd_file) as keyfile:
    encrypted_key = keyfile.read()
    private_key = conn.eth.account.decrypt(encrypted_key, bc_pwd_file_pwd)
