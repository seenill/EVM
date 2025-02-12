from web3 import Web3
import os

# 初始化 Web3 连接到以太坊节点，根据实际情况修改节点地址
infura_url = os.getenv("web3_conn_infura_url")
web3 = Web3(Web3.HTTPProvider(infura_url))
def get_block_data(block_number):
    """
    从节点获取指定区块号的区块数据
    :param block_number: 区块号
    :return: 包含区块数据的字典和交易哈希列表
    """
    try:
        block = web3.eth.get_block(block_number)
        block_data = {
            'block_height': block.number,
            'version_number': 0,  # 以太坊没有明确的版本号概念，设为 0
            'previous_block_hash': web3.to_hex(block.parentHash),
            'merkle_root': web3.to_hex(block.hash),
            'timestamp': block.timestamp,
            'difficulty_target': block.difficulty,
            'nonce': block.nonce,
            'miner_address': block.miner,
            'signature': ""  # 以太坊区块没有单独的签名信息，设为空字符串
        }
        transaction_hashes = [web3.to_hex(tx_hash) for tx_hash in block.transactions]
        return block_data, transaction_hashes
    except Exception as e:
        print(f"获取区块数据时出错: {e}")
        return None, []