package res

type TransactionModel struct {
	BlockNumberANDTransactionIndex uint64 `gorm:"column:block_number_and_transaction_index;primaryKey;not null" json:"block_number_and_transaction_index"`
	ChainID                        uint64 `gorm:"column:chain_id;not null" json:"chain_id"`                       // 网络链ID
	Hash                           string `gorm:"column:hash;type:char(66);unique;not null" json:"hash"`          // 交易哈希，唯一标识
	From                           string `gorm:"column:from_address;type:char(42);not null" json:"from_address"` // 发送方地址，修改列名避免关键字冲突
	To                             string `gorm:"column:to_address;type:char(42)" json:"to_address"`              // 接收方地址
	Value                          string `gorm:"column:value;not null" json:"value"`                             // 交易金额
	Gas                            uint64 `gorm:"column:gas;not null" json:"gas"`                                 // 交易使用的气体量
	GasPrice                       string `gorm:"column:gas_price;not null" json:"gas_price"`                     // 气体价格
	Nonce                          uint64 `gorm:"column:nonce;not null" json:"nonce"`                             // 交易的随机数
	BlockHash                      string `gorm:"column:block_hash;type:char(66);not null" json:"block_hash"`     // 包含该交易的区块哈希
	BlockNumber                    uint64 `gorm:"column:block_number;not null" json:"block_number"`               // 包含该交易的区块编号
	TransactionIndex               uint64 `gorm:"column:transaction_index;not null" json:"transaction_index"`     // 交易在区块内的索引
	Input                          []byte `gorm:"column:input;type:longblob" json:"input"`                        // 交易输入数据
	V                              string `gorm:"column:v;not null" json:"v"`                                     // 签名参数 V
	R                              string `gorm:"column:r;not null" json:"r"`                                     // 签名参数 R
	S                              string `gorm:"column:s;not null" json:"s"`                                     // 签名参数 S
}
