import os

import redis

# 连接 Redis
redis_client = redis.Redis(host=os.getenv("redis_host"), port= int(os.getenv("redis_port")), db=int(os.getenv("redis_db")))

def get_log_hash():
    """从 Redis 集合 log_key 中获取一个 log 对应的 hash 值"""
    log_hash = redis_client.spop(os.getenv("log_key"))
    if log_hash:
        return log_hash
    return None

def remove_log_hash(log_hash):
    """从 Redis 集合 log_key 中移除指定的 log hash 值"""
    redis_client.srem(os.getenv("log_key"), log_hash)