from web3 import Web3
from blockchain.account.addr import addr


# web3.eth.sign()方法使用指定的账户对数据进行签名，该账户必须先解锁。

# dataToSign：String - 待签名的数据。对于字符串将首先使用web3.utils.utf8ToHex()
# 方法将其转换为16进制
# address：String | Number - 用来签名的账户地址。或者本地钱包web3.eth.accounts.wallet中的地址或其序号
# callback：Function - 可选的回调函数，其第一个参数为错误对象，第二个参数为结果

def web3_sign(dataToSign, address=addr, callback=None):
    dataToSign = Web3.toHex(dataToSign)
    Web3.eth.sign(dataToSign, address, callback)
