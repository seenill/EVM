import redis

# 连接到 Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_transaction_hash_from_redis():
    """从 Redis 集合中随机获取一个交易哈希并移除"""
    transaction_hash = redis_client.spop('transaction_key')
    if transaction_hash:
        return transaction_hash.decode('utf-8')
    return None