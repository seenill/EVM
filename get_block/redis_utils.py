import os

import redis

# 初始化 Redis 连接
redis_client = redis.Redis(host=os.getenv("redis_host"), port= int(os.getenv("redis_port")), db=int(os.getenv("redis_db")))

def get_block_numbers():
    """
    从 Redis 的 block_number 集合中获取所有区块号
    :return: 包含区块号的集合
    """
    block_numbers = redis_client.smembers(os.getenv('block_key'))
    return block_numbers

def add_transaction_hashes(transaction_hashes):
    """
    将交易哈希添加到 Redis 的 transaction_key 集合中
    :param transaction_hashes: 交易哈希列表
    """
    for tx_hash in transaction_hashes:
        redis_client.sadd(os.getenv('transaction_key'), tx_hash)
        redis_client.sadd(os.getenv('receipt_key'), tx_hash)

def remove_block_number(block_number):
    """
    从 Redis 的 block_number 集合中移除指定的区块号
    :param block_number: 要移除的区块号
    """
    redis_client.srem(os.getenv('block_key'), block_number)