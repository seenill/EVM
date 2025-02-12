import os

from web3 import Web3

# 连接以太坊节点，根据实际情况修改节点地址
infura_url = os.getenv("web3_conn_infura_url")  # 请替换为你的节点地址
web3 = Web3(Web3.LegacyWebSocketProvider(infura_url))

def get_logs_from_receipt(transaction_hash):
    """根据交易哈希获取交易收据并提取所有日志信息"""
    try:
        receipt = web3.eth.get_transaction_receipt(transaction_hash)
        logs = []
        for log in receipt.logs:
            log_data = {
                'log_index': log.logIndex,
                'block_number_and_transaction_index': int(f"{receipt.blockNumber}{receipt.transactionIndex}"),
                'address': log.address,
                'transaction_hash': web3.to_hex(log.transactionHash),
                'topics0': web3.to_hex(log.topics[0]) if log.topics else None,
                'topics1': web3.to_hex(log.topics[1]) if len(log.topics) > 1 else None,
                'topics2': web3.to_hex(log.topics[2]) if len(log.topics) > 2 else None,
                'topics3': web3.to_hex(log.topics[3]) if len(log.topics) > 3 else None,
                'data': web3.to_hex(log.data) if log.data else None
            }
            logs.append(log_data)
        return logs
    except Exception as e:
        print(f"获取日志数据时出错: {e}")
        return []