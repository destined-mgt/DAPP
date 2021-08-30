from blockchain.connecter.connecter import conn
from blockchain.contract.workArg.config_abi import abi
from blockchain.contract.workArg.config_addr import addr

contract = conn.eth.contract(address=conn.toChecksumAddress(addr), abi=abi)
