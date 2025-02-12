package res

type BlockModel struct {
	BlockHeight       uint64 `gorm:"column:block_height;primaryKey;not null" json:"block_height"`
	VersionNumber     int    `gorm:"column:version_number;not null" json:"version_number"`
	PreviousBlockHash string `gorm:"column:previous_block_hash;type:char(70);not null" json:"previous_block_hash"`
	MerkleRoot        string `gorm:"column:merkle_root;type:char(66);not null" json:"merkle_root"`
	Timestamp         int    `gorm:"column:timestamp;not null" json:"timestamp"`
	DifficultyTarget  int    `gorm:"column:difficulty_target;not null" json:"difficulty_target"`
	Nonce             int    `gorm:"column:nonce;not null" json:"nonce"`
	MinerAddress      string `gorm:"column:miner_address;not null" json:"miner_address"`
	Signature         string `gorm:"column:signature;not null" json:"signature"` //暂时设空
}
