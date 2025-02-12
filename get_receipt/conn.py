import os

from web3 import Web3, AsyncWeb3

# 替换为你的 Infura 项目 ID 或节点地址
infura_url = os.getenv("web3_conn_infura_url")  # 请替换为你的节点地址
w3 = Web3(Web3.LegacyWebSocketProvider(infura_url))

# 检查是否成功连接到节点
if w3.is_connected():
    print("成功连接到以太坊节点")
else:
    print("无法连接到以太坊节点")

def get_receipt_details(transaction_hash):
    try:
        receipt = w3.eth.get_transaction_receipt(transaction_hash)
        if receipt:
            receipt_details = {
                'block_number_and_transaction_index': receipt.get('blockNumber') * 10000 + receipt.get('transactionIndex'),
                'transaction_hash': receipt.get('transactionHash').hex(),
                'block_hash': receipt.get('blockHash').hex(),
                'block_number': receipt.get('blockNumber'),
                'transaction_index': receipt.get('transactionIndex'),
                'status': receipt.get('status'),
                'cumulative_gas_used': receipt.get('cumulativeGasUsed'),
                'gas_used': receipt.get('gasUsed'),
                'contract_address': receipt.get('contractAddress'),
                'logs_bloom': receipt.get('logsBloom').hex()
            }
            return receipt_details
        else:
            print(f"未找到交易哈希 {transaction_hash} 的相关信息")
    except Exception as e:
        print(f"获取交易收据详情时出错: {e}")
    return None