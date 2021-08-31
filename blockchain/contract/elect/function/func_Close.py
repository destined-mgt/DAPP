from blockchain.connecter.connecter import conn, private_key
from blockchain.account.addr import addr
from blockchain.contract.elect.conn_elect import contract
from utility import Log


def Close(mag):
    Log.logger.info("call function: Elect.Close")
    nonce = conn.eth.getTransactionCount(addr)
    try:
        gas = contract.functions.Reply(mag).estimateGas()
        tx = contract.functions.Reply(mag).buildTransaction({
            'chainId': conn.eth.chainId,
            'gas': gas * 2,
            'gasPrice': conn.eth.gasPrice,
            'nonce': nonce,
        })
        # 交易签名
        signed_tx = conn.eth.account.sign_transaction(tx, private_key)
        # 发往区块链
        conn.eth.sendRawTransaction(signed_tx.rawTransaction)
        # 等待交易返回
        conn.eth.waitForTransactionReceipt(signed_tx.hash)
        # 打印交易哈希
        tx_hash = conn.toHex(conn.keccak(signed_tx.rawTransaction))
        return_value = {
            'tx_hash': tx_hash,
            'error': None
        }
        print(return_value)
        return return_value
    except Exception as e:
        print(e)
        return_value = {
            'tx_hash': None,
            'error': e.__str__()
        }
        return return_value
