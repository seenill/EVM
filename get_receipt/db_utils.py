import os

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT
# 数据库配置
DB_USER = os.environ.get("mysql_user")
DB_PASSWORD = os.environ.get("mysql_password")
DB_HOST = os.environ.get("mysql_host")
DB_NAME = os.environ.get("mysql_db_name")
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class ReceiptModel(Base):
    __tablename__ = 'receipt_models'
    # 定义列
    block_number_and_transaction_index = Column(BIGINT(unsigned=True), primary_key=True, nullable=False)
    transaction_hash = Column(String(66), nullable=False, unique=True)
    block_hash = Column(String(66), nullable=False)
    block_number = Column(BIGINT(unsigned=True), nullable=False)
    transaction_index = Column(BIGINT(unsigned=True), nullable=False)
    status = Column(BIGINT(unsigned=True), nullable=False)
    cumulative_gas_used = Column(BIGINT(unsigned=True), nullable=False)
    gas_used = Column(BIGINT(unsigned=True), nullable=False)
    contract_address = Column(String(42), nullable=True)
    logs_bloom = Column(Text, nullable=True)
def save_receipt_to_db(receipt_details):
    """将交易收据详情保存到数据库"""
    # 创建 ReceiptModel 实例
    receipt = ReceiptModel(**receipt_details)
    try:
        # 尝试插入新记录
        session.add(receipt)
        session.commit()
        print("插入成功")
        return True
    except IntegrityError:
        # 主键冲突，回滚会话
        session.rollback()
        # 删除原记录
        existing_receipt = session.query(ReceiptModel).filter_by(
            block_number_and_transaction_index=receipt.block_number_and_transaction_index
        ).first()
        if existing_receipt:
            session.delete(existing_receipt)
            session.commit()
        # 再次尝试插入新记录
        try:
            session.add(receipt)
            session.commit()
            print("删除原记录后插入成功")
            return True
        except Exception as e:
            session.rollback()
            print(f"保存交易收据详情到数据库时出错: {e}")
            return False
