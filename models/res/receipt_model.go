package res

// ReceiptModel 表示区块链中的交易回执
type ReceiptModel struct {
	BlockNumberANDTransactionIndex uint64 `gorm:"column:block_number_and_transaction_index;primaryKey;not null" json:"block_number_and_transaction_index"`
	TransactionHash                string `gorm:"column:transaction_hash;type:char(66);unique;not null" json:"transaction_hash"` // 关联的交易哈希
	BlockHash                      string `gorm:"column:block_hash;type:char(66);not null" json:"block_hash"`                    // 包含该交易的区块哈希
	BlockNumber                    uint64 `gorm:"column:block_number;not null" json:"block_number"`                              // 包含该交易的区块编号
	TransactionIndex               uint64 `gorm:"column:transaction_index;not null" json:"transaction_index"`                    // 交易在区块内的索引
	Status                         uint64 `gorm:"column:status;not null" json:"status"`                                          // 交易状态，如 1 表示成功，0 表示失败
	CumulativeGasUsed              uint64 `gorm:"column:cumulative_gas_used;not null" json:"cumulative_gas_used"`                // 累积气体使用量
	GasUsed                        uint64 `gorm:"column:gas_used;not null" json:"gas_used"`                                      // 本次交易使用的气体量
	ContractAddress                string `gorm:"column:contract_address;type:char(42)" json:"contract_address"`                 // 合约地址（如果是合约创建交易）
	LogsBloom                      string `gorm:"column:logs_bloom;type:text" json:"logs_bloom"`                                 // 布隆过滤器
}
