import os

import redis

# 连接到 Redis
redis_client = redis.Redis(host=os.getenv("redis_host"), port= int(os.getenv("redis_port")), db=int(os.getenv("redis_db")))

def get_transaction_hash_from_redis():
    """从 Redis 集合中随机获取一个交易哈希并移除"""
    transaction_hash = redis_client.spop('receipt_key')
    if transaction_hash:
        return transaction_hash.decode('utf-8')
    return None

def put_log_transaction_hash_from_redis(transaction_hash ):
    redis_client.sadd(os.getenv("log_key"), transaction_hash)
    return None