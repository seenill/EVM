import os

import redis

# 连接到 Redis
redis_client = redis.Redis(host=os.getenv("redis_host"), port= int(os.getenv("redis_port")), db=int(os.getenv("redis_db")))

def get_transaction_hash_from_redis():
    """从 Redis 集合中随机获取一个交易哈希，若该次循环结束时没有报错则移除"""
    # 先随机获取一个交易哈希，但不移除
    transaction_hash = redis_client.srandmember(os.getenv("transaction_key"))
    if transaction_hash:
        return transaction_hash.decode('utf-8')
    return None

def remove_transaction_hash_from_redis(transaction_hash):
    """在该次循环结束时，如果没有报错则移除交易哈希"""
    if transaction_hash:
        # 将交易哈希编码为字节类型
        encoded_hash = transaction_hash.encode('utf-8')
        # 移除指定的交易哈希
        redis_client.srem(os.getenv("transaction_key"), encoded_hash)
        redis_client.sadd(os.getenv("log_key"), encoded_hash)
