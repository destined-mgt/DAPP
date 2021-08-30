from blockchain.connecter.connecter import conn, private_key
from blockchain.account.addr import addr
from blockchain.contract.work.conn_work import contract


def SubmitModel(mag, model):
    print("call function: Work.SubmitModel")
    nonce = conn.eth.getTransactionCount(addr)
    try:
        gas = contract.functions.SubmitModel(mag, model).estimateGas()
        tx = contract.functions.SubmitModel(mag, model).buildTransaction({
            'chainId': conn.eth.chainId,
            'gas': gas * 10,
            'gasPrice': conn.eth.gasPrice * 2,
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
