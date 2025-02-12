import time
from redis_utils import get_log_hash, remove_log_hash
from block_fetcher import get_logs_from_receipt
from mysql_utils import insert_log_data, close_mysql_connection

def process_transaction_hashes():
    while True:
        # 从 Redis 获取一个交易哈希
        transaction_hash_byte = get_log_hash()
        print(transaction_hash_byte)
        if not transaction_hash_byte:
            # 如果没从 Redis 拿到交易哈希，休眠 20 秒
            time.sleep(20)
            continue

        transaction_hash = transaction_hash_byte.decode('utf-8')

        # 根据交易哈希获取日志信息
        logs = get_logs_from_receipt(transaction_hash)
        if logs:
            success = True
            for log in logs:
                # 将日志数据插入数据库
                if not insert_log_data(log):
                    success = False
                    break

            if success:
                # 存入成功后从 Redis 移除处理过的交易哈希
                remove_log_hash(transaction_hash)


if __name__ == "__main__":
    try:
        process_transaction_hashes()
    except KeyboardInterrupt:
        print("程序终止")
    finally:
        # 关闭 MySQL 连接
        close_mysql_connection()