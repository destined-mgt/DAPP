from blockchain.connecter.connecter import conn, private_key
from blockchain.account.addr import addr
from blockchain.contract.work.conn_work import contract
from utility import Log


def GetModelToMerge(mag):
    Log.logger.info("call function: Work.GetModelToMerge")
    nonce = conn.eth.getTransactionCount(addr)
    try:
        models = contract.functions.GetModelsToMerge(mag).call()
        gas = contract.functions.GetModelsToMerge(mag).estimateGas()
        tx = contract.functions.GetModelsToMerge(mag).buildTransaction({
            'chainId': conn.eth.chainId,
            'gas': gas * 3,

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
        # 获取交易回执

        return_value = {
            'tx_hash': tx_hash,
            'models': models,
            'error': None
        }
        print(return_value)
        return return_value
    except Exception as e:
        print(e)
        return_value = {
            'tx_hash': None,
            'models': None,
            'error': e.__str__()
        }
        return return_value
