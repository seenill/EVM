import time

from redis_utils import get_transaction_hash_from_redis,remove_transaction_hash_from_redis
from conn import get_transaction_details
from db_utils import save_transaction_to_db, Base, session

if __name__ == "__main__":
    while True:

        # 从 Redis 中获取交易哈希
        transaction_hash = get_transaction_hash_from_redis()
        if transaction_hash:
            print(f"获取到交易哈希: {transaction_hash}")
            # 解析交易哈希，获取交易详细信息
            transaction_details = get_transaction_details(transaction_hash)
            if transaction_details:
                print("交易详细信息:")
                for key, value in transaction_details.items():
                    print(f"{key}: {value}")
                # 将交易详情保存到数据库 log被加入redis
                if save_transaction_to_db(transaction_details):
                    remove_transaction_hash_from_redis(transaction_hash)
                    print(f"交易哈希 {transaction_hash} 已从 Redis 集合中移除。")
            else:
                print("无法解析交易哈希，获取交易详细信息失败。")
        else:
            print("Redis 集合中没有可用的交易哈希。")
            time.sleep(20)
