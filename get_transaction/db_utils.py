import os

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base
# 数据库配置
DB_USER = os.environ.get("mysql_user")
DB_PASSWORD = os.environ.get("mysql_password")
DB_HOST = os.environ.get("mysql_host")
DB_NAME = os.environ.get("mysql_db_name")
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class Transaction(Base):
    __tablename__ = 'transaction_models'
    block_number_and_transaction_index = Column(Integer, primary_key=True, autoincrement=True)
    chain_id = Column(Integer, nullable=False)
    hash = Column(String(66), unique=True, nullable=False)
    from_address = Column(String(42), nullable=False)
    to_address = Column(String(42))
    value = Column(String(255), nullable=False)
    gas = Column(Integer, nullable=False)
    gas_price = Column(String(255), nullable=False)
    nonce = Column(Integer, nullable=False)
    block_hash = Column(String(66), nullable=False)
    block_number = Column(Integer, nullable=False)
    transaction_index = Column(Integer, nullable=False)
    input = Column(LargeBinary)
    v = Column(String(255), nullable=False)
    r = Column(String(255), nullable=False)
    s = Column(String(255), nullable=False)
def save_transaction_to_db(transaction_details):
    """将交易详情保存到数据库"""
    transaction = Transaction(**transaction_details)
    try:
        # 尝试插入新记录
        session.add(transaction)
        session.commit()
        print("插入成功")
        return True
    except IntegrityError:
        # 主键冲突，回滚会话
        session.rollback()
        # 删除原记录
        existing_transaction = session.query(Transaction).filter_by(
            block_number_and_transaction_index=transaction.block_number_and_transaction_index
        ).first()
        if existing_transaction:
            session.delete(existing_transaction)
            session.commit()
        # 再次尝试插入新记录
        try:
            session.add(transaction)
            session.commit()
            print("删除原记录后插入成功")
            return True
        except Exception as e:
            session.rollback()
            print(f"保存交易详情到数据库时出错: {e}")
            return False