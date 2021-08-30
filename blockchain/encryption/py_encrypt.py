from _pysha3 import keccak_256


# 生成公私钥
def GenSecretsPair():
    from coincurve import PrivateKey
    p = PrivateKey()
    return p.to_hex(), p.public_key.format(compressed=False).hex()


# keccak256 哈希
def Hasher(msg_str):
    k = keccak_256()
    k.update(msg_str.encode("utf-8"))
    return k.hexdigest()


# 签名
def Sign(hash_msg_str, pk_str):
    from coincurve import PrivateKey
    pk = PrivateKey(bytearray.fromhex(pk_str))
    return pk.sign_recoverable(bytes(bytearray.fromhex(hash_msg_str)), hasher=None).hex()


# 验证签名
def Decode(sig_msg_str, msg_str):
    from coincurve import PublicKey
    pk = PublicKey.from_signature_and_message(bytes(bytearray.fromhex(sig_msg_str)), bytes(bytearray.fromhex(msg_str)),
                                              hasher=None)
    return pk.format(compressed=False).hex()
