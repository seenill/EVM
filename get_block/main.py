import time
from redis_utils import get_block_numbers, add_transaction_hashes, remove_block_number
from mysql_utils import insert_block_data, close_mysql_connection
from block_fetcher import get_block_data

def process_block_number():
    """
    主处理逻辑，每隔 20 秒检查 Redis 中的 block_number 集合
    """
    while True:
        # 从 Redis 获取区块号
        block_numbers = get_block_numbers()
        if block_numbers:
            print(block_numbers)
            for block_number_bytes in block_numbers:
                block_number = int(block_number_bytes.decode('utf-8'))
                # 获取区块数据和交易哈希
                block_data, transaction_hashes = get_block_data(block_number)
                print(block_data)
                if block_data:
                    # 插入区块数据到 MySQL
                    insert_block_data(block_data)
                    # 将交易哈希存入 Redis
                    add_transaction_hashes(transaction_hashes)
                    # 从 Redis 移除处理过的区块号
                    remove_block_number(block_number)
        # 每隔 20 秒检查一次
        time.sleep(20)

if __name__ == "__main__":
    try:
        process_block_number()
    except KeyboardInterrupt:
        print("程序终止")
    finally:
        # 关闭 MySQL 连接
        close_mysql_connection()