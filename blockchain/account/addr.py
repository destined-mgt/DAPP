import json

from web3 import Web3

from utility.ParseConfig import GetConfig

cfg = GetConfig("config")
bc_pwd_file = cfg.get("SYSTEM", "bc_pwd_file")

with open(bc_pwd_file) as file:
    jsonFile = json.load(file)
    addrFromPwd = jsonFile['address']
    addr = Web3.toChecksumAddress(addrFromPwd)
