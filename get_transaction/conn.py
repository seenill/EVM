import os

from web3 import Web3, AsyncWeb3

# 替换为你的 Infura 项目 ID
from web3 import Web3

# 替换为你的 Infura 项目 ID
infura_url = os.getenv("web3_conn_infura_url")   # 请替换为你的节点地址
w3 = Web3(Web3.LegacyWebSocketProvider(infura_url))

# 检查是否成功连接到节点
if w3.is_connected():
    print("成功连接到以太坊节点")
else:
    print("无法连接到以太坊节点")

def get_transaction_details(transaction_hash):
    try:
        transaction = w3.eth.get_transaction(transaction_hash)
        block_number_and_transaction_index=transaction.get('blockNumber')*10000+transaction.get('transactionIndex')
        if transaction:
            transaction_details = {
                'block_number_and_transaction_index':block_number_and_transaction_index,
                'chain_id': transaction.get('chainId'),
                'hash': transaction.get('hash').hex(),
                'from_address': transaction.get('from'),
                'to_address': transaction.get('to'),
                'value': str(transaction.get('value')),
                'gas': transaction.get('gas'),
                'gas_price': str(transaction.get('gasPrice')),
                'nonce': transaction.get('nonce'),
                'block_hash': transaction.get('blockHash').hex(),
                'block_number': transaction.get('blockNumber'),
                'transaction_index': transaction.get('transactionIndex'),
                'input': transaction.get('input'),
                'v': str(transaction.get('v')),
                'r': transaction.get('r').hex(),
                's': transaction.get('s').hex()
            }
            return transaction_details
        else:
            print(f"未找到交易哈希 {transaction_hash} 的相关信息")
    except Exception as e:
        print(f"获取交易详情时出错: {e}")
    return None