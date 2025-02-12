package transaction_type

import (
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"math/big"
)

// 不行
// getFrom 函数用于从 EIP - 4844 交易中获取发送方地址
func GetFrom(tx *types.Transaction, chainID *big.Int) (common.Address, error) {
	// EIP - 4844 交易使用 EIP - 155 签名方案
	signer := types.NewEIP155Signer(chainID)
	// 从交易的签名中恢复发送方地址
	from, err := types.Sender(signer, tx)
	if err != nil {
		return common.Address{}, err
	}
	return from, nil
}
