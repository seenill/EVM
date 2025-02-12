import time

from receipt_utils import get_transaction_hash_from_redis, put_log_transaction_hash_from_redis
from conn import get_receipt_details
from db_utils import save_receipt_to_db, Base, session

if __name__ == "__main__":
    # 创建表（如果不存在）

    while True:
        # 从 Redis 中获取交易哈希
        transaction_hash = get_transaction_hash_from_redis()
        if transaction_hash:
            print(f"获取到交易哈希: {transaction_hash}")
            # 解析交易哈希，获取交易收据详细信息
            receipt_details = get_receipt_details(transaction_hash)
            if receipt_details:
                for key, value in receipt_details.items():
                    # 这里可以根据需要处理键值对，暂时保留原样
                    pass
                # 将交易收据详情保存到数据库
                if save_receipt_to_db(receipt_details):
                    put_log_transaction_hash_from_redis(transaction_hash)
                    print(f"交易哈希 {transaction_hash} 已从 Redis 集合中移除。")
            else:
                print("无法解析交易哈希，获取交易收据详细信息失败。")
        else:
            print("Redis 集合中没有可用的交易哈希。")
            time.sleep(20)