package res

type LogModel struct {
	ID                             uint64 `gorm:"primary_key;auto_increment" json:"id"`
	LogIndex                       uint64 `gorm:"column:log_index;not null"`                             // log在logs里的序号
	BlockNumberANDTransactionIndex uint64 `gorm:"column:block_number_and_transaction_index;not null"`    // 关联的交易回执 ID
	Address                        string `gorm:"column:address;type:char(42);not null"`                 // 触发日志的合约地址
	TransactionHash                string `gorm:"column:transaction_hash;type:char(66);unique;not null"` // 关联的交易哈希
	// AI说一条日志中只能有4个主题
	Topics0 *string `gorm:"column:topics0;type:text"` // 日志主题，可存储为 JSON 数组字符串
	Topics1 *string `gorm:"column:topics1;type:text"` // 日志主题，可存储为 JSON 数组字符串
	Topics2 *string `gorm:"column:topics2;type:text"` // 日志主题，可存储为 JSON 数组字符串
	Topics3 *string `gorm:"column:topics3;type:text"` // 日志主题，可存储为 JSON 数组字符串
	Data    string  `gorm:"column:data;type:text"`    // 日志数据
}
