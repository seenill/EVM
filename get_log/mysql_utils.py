import os

from sqlalchemy import create_engine, Column, BigInteger, String, Text, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT

# 数据库连接配置
DB_USER = os.getenv("mysql_user")
DB_PASSWORD = os.getenv("mysql_password")
DB_NAME = os.getenv("mysql_db_name")
DB_HOST = os.getenv("mysql_host")
DB_PORT = int(os.getenv("mysql_port"))

# 构建数据库连接字符串
DB_CONNECTION_STRING = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# 创建数据库引擎
engine = create_engine(DB_CONNECTION_STRING)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class LogModel(Base):
    __tablename__ = 'log_models'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    log_index = Column(BIGINT(unsigned=True), nullable=False)
    block_number_and_transaction_index = Column(BIGINT(unsigned=True), nullable=False)
    address = Column(String(42), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    topics0 = Column(Text, nullable=True)
    topics1 = Column(Text, nullable=True)
    topics2 = Column(Text, nullable=True)
    topics3 = Column(Text, nullable=True)
    data = Column(Text, nullable=True)

    # 创建联合索引
    __table_args__ = (
        Index('block_number_and_transaction_index_and_log_index', 'block_number_and_transaction_index', 'log_index'),
        Index('transaction_hash_and_log_index', 'transaction_hash', 'log_index')
    )

def insert_log_data(log_data):
    """将日志数据插入到数据库的 log_models 表中"""
    session = Session()
    try:
        new_log = LogModel(**log_data)
        session.add(new_log)
        session.commit()
    except Exception as e:
        print(f"插入日志数据到 MySQL 时出错: {e}")
        session.rollback()
    finally:
        session.close()

def close_mysql_connection():
    """关闭数据库连接（对于 SQLAlchemy 这里没有显式关闭引擎的必要，因为它会自动管理连接池）"""
    pass