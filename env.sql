use transaction_data;
CREATE TABLE log_models (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                             log_index BIGINT UNSIGNED NOT NULL,
                             block_number_and_transaction_index BIGINT UNSIGNED NOT NULL,
                             address CHAR(42) NOT NULL,
                             transaction_hash CHAR(66) NOT NULL,
                             topics0 TEXT NULL,
                             topics1 TEXT NULL,
                             topics2 TEXT NULL,
                             topics3 TEXT NULL,
                             data TEXT NULL,
    -- 创建联合索引，block_number_and_transaction_index 在前
                             INDEX block_number_and_transaction_index_and_log_index (block_number_and_transaction_index, log_index),
    -- 创建联合索引，transaction_hash 在前
                             INDEX  transaction_hash_and_log_index(transaction_hash, log_index)
);


create table receipt_models
(
    block_number_and_transaction_index bigint unsigned not null
        primary key,
    transaction_hash                   char(66)        not null,
    block_hash                         char(66)        not null,
    block_number                       bigint unsigned not null,
    transaction_index                  bigint unsigned not null,
    status                             bigint unsigned not null,
    cumulative_gas_used                bigint unsigned not null,
    gas_used                           bigint unsigned not null,
    contract_address                   char(42)        null,
    logs_bloom                         text            null,
    constraint transaction_hash
        unique (transaction_hash)
);

create index idx_transaction_hash
    on receipt_models (transaction_hash);

create table transaction_models
(
    block_number_and_transaction_index bigint unsigned not null
        primary key,
    chain_id                           bigint unsigned not null,
    hash                               char(66)        not null,
    `from_address`                             char(42)        not null,
    `to_address`                               char(42)        null,
    value                              text            not null,
    gas                                bigint unsigned not null,
    gas_price                          text            not null,
    nonce                              bigint unsigned not null,
    block_hash                         char(66)        not null,
    block_number                       bigint unsigned not null,
    transaction_index                  bigint unsigned not null,
    input                              longblob            null,
    v                                  text            not null,
    r                                  text            not null,
    s                                  text            not null,
    constraint hash
        unique (hash)
);

create index idx_hash
    on transaction_models (hash);



-- 创建 blocks 表来存储区块链区块信息
CREATE TABLE block_models (
    -- 区块高度，采用整数类型存储
                        block_height INT unsigned not null,
    -- 区块版本号，采用整数类型存储
                        version_number INT NOT NULL,
    -- 前一区块哈希，采用固定长度的字符类型存储
                        previous_block_hash CHAR(70) NOT NULL,
    -- 梅克尔根，采用固定长度的字符类型存储
                        merkle_root CHAR(70) NOT NULL,
    -- 时间戳，采用整数类型存储 Unix 时间戳
                        timestamp INT NOT NULL,
    -- 难度目标，采用整数类型存储
                        difficulty_target INT NOT NULL,
    -- 随机数，采用整数类型存储
                        nonce INT NOT NULL,
    -- 矿工地址，采用固定长度的字符类型存储
                        miner_address CHAR(43) NOT NULL,
    -- 签名信息，采用文本类型存储
                        signature TEXT NOT NULL
);