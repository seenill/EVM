import os

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from web3.types import HexBytes  # 导入 HexBytes 类型

# 数据库连接配置
DB_USER = os.environ.get("mysql_user")
DB_PASSWORD = os.environ.get("mysql_password")
DB_HOST = os.environ.get("mysql_host")
DB_NAME = os.environ.get("mysql_db_name")
DB_CONNECTION_STRING = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# 创建数据库引擎
engine = create_engine(DB_CONNECTION_STRING)
Base = sqlalchemy.orm.declarative_base()
Session = sessionmaker(bind=engine)

# 定义 BlockModel 类，对应数据库中的 block_models 表
class BlockModel(Base):
    __tablename__ = 'block_models'
    block_height = Column(Integer, primary_key=True, nullable=False)
    version_number = Column(Integer, nullable=False)
    previous_block_hash = Column(String(70), nullable=False)
    merkle_root = Column(String(70), nullable=False)
    timestamp = Column(Integer, nullable=False)
    difficulty_target = Column(Integer, nullable=False)
    nonce = Column(Integer, nullable=False)
    miner_address = Column(String(43), nullable=False)
    signature = Column(Text, nullable=False)

def insert_block_data(block_data):
    """
    将区块数据插入到数据库的 block_models 表中
    :param block_data: 包含区块数据的字典
    """
    session = Session()
    try:
        # 检查 nonce 是否为 HexBytes 类型，如果是则转换为整数
        if isinstance(block_data['nonce'], HexBytes):
            block_data['nonce'] = int(block_data['nonce'].hex(), 16)
        # 先查询是否存在相同 block_height 的记录
        existing_block = session.query(BlockModel).filter_by(block_height=block_data['block_height']).first()
        if existing_block:
            print(f"Block with height {block_data['block_height']} already exists. Skipping insertion.")
        else:
            new_block = BlockModel(**block_data)
            session.add(new_block)
            session.commit()
    except Exception as e:
        print(f"插入区块数据到 MySQL 时出错: {e}")
        session.rollback()
    finally:
        session.close()

def close_mysql_connection():
    engine.dispose()