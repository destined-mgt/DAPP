from blockchain.connecter.connecter import conn
from blockchain.contract.elect.config_abi import abi
from blockchain.contract.elect.config_addr import addr

contract = conn.eth.contract(address=conn.toChecksumAddress(addr), abi=abi)
