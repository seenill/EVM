package EVM

import (
	"SeeEVM/global"
	"SeeEVM/models"
	"SeeEVM/models/res"
	"context"
	"encoding/hex"
	"fmt"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
	"log"
	"time"
)

// 可能要分开存因为2个请求时间比较长
// ProcessTransactionLogs 处理单个交易的receipt
func ProcessTransactionLogs(client *ethclient.Client, txHash common.Hash) {

	//等待处理状态没必要拿
	tx, _, err := client.TransactionByHash(context.Background(), txHash)
	if err != nil {
		log.Printf("获取交易 %s 的交易时出错: %v", txHash.Hex(), err)
		//把Hash存到Redis
		err := global.Redis.SAdd(TransactionKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
		}
		err = global.Redis.SAdd(ReceiptKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
		}
		return
	}
	time.Sleep(100 * time.Millisecond) // 增加 100 毫秒的延迟
	receipt, err := client.TransactionReceipt(context.Background(), txHash)
	if receipt == nil {
		log.Printf("获取交易 %s 的收据时出错: %v", txHash.Hex(), err)
		//把Hash存到redis
		err := global.Redis.SAdd(ReceiptKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
			return
		}
		return
	}
	//var blockNumberANDTransactionIndex uint64
	// 组合区块编号和交易索引
	blockNumberANDTransactionIndex := receipt.BlockNumber.Uint64()*10000 + uint64(receipt.TransactionIndex)
	customReceipt := res.ReceiptModel{
		BlockNumberANDTransactionIndex: blockNumberANDTransactionIndex,
		TransactionHash:                receipt.TxHash.Hex(),
		BlockHash:                      receipt.BlockHash.Hex(),
		BlockNumber:                    receipt.BlockNumber.Uint64(),
		TransactionIndex:               uint64(receipt.TransactionIndex),
		Status:                         receipt.Status,
		CumulativeGasUsed:              receipt.CumulativeGasUsed,
		GasUsed:                        receipt.GasUsed,
		ContractAddress:                receipt.ContractAddress.Hex(),
		LogsBloom:                      hex.EncodeToString(receipt.Bloom[:]),
	}
	//to不一定有
	to := ""
	if tx.To() != nil {
		to = tx.To().Hex()
	}
	v, r, s := tx.RawSignatureValues()
	vStr := v.Text(16)
	rStr := r.Text(16)
	sStr := s.Text(16)

	signer := types.NewLondonSigner(tx.ChainId())
	switch tx.Type() {
	case types.DynamicFeeTxType:
		signer = types.NewLondonSigner(tx.ChainId())
	case types.BlobTxType: // EIP - 4844 交易类型
		{
			fmt.Println(1)
			err := global.Redis.SAdd("transaction", txHash.Hex()).Err()
			if err != nil {
				fmt.Printf("Failed to add value to set: %v\n", err)
				return
			}
		}
	default:
		signer = types.NewEIP155Signer(tx.ChainId())
	}
	fromStr := ""
	// 获取发送方地址
	from, err := signer.Sender(tx)
	if err != nil {
		//存入redis
		err := global.Redis.SAdd(TransactionKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
		}
		return
	}
	fromStr = from.Hex()

	// 创建 Transaction 结构体实例并填充信息
	transaction := res.TransactionModel{
		BlockNumberANDTransactionIndex: blockNumberANDTransactionIndex,
		Hash:                           tx.Hash().Hex(),
		ChainID:                        tx.ChainId().Uint64(),
		Value:                          tx.Value().String(),
		To:                             to,
		From:                           fromStr,
		Gas:                            tx.Gas(),
		GasPrice:                       tx.GasPrice().String(),
		Nonce:                          tx.Nonce(),
		BlockHash:                      receipt.BlockHash.Hex(),
		BlockNumber:                    receipt.BlockNumber.Uint64(),
		TransactionIndex:               uint64(receipt.TransactionIndex),
		Input:                          tx.Data(),
		V:                              vStr,
		R:                              rStr,
		S:                              sStr,
	}
	//入库逻辑
	//感觉没必要传TransactionHash
	//Receipt
	TransactionHash, err := models.InsertReceipt(global.DB, customReceipt) //如果报错都是把错误hash传到redis
	if err != nil {
		log.Printf("Receipt存入数据库时 %s 时出错: %v", TransactionHash, err)
		//把Hash存到redis
		err := global.Redis.SAdd(ReceiptKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
		}
	}
	//transaction
	TransactionHash, err = models.InsertTransaction(global.DB, transaction) //如果报错都是把错误hash传到redis
	if err != nil {
		log.Printf("Transaction存入数据库时 %s 时出错: %v", TransactionHash, err)
		//把Hash存到redis
		err := global.Redis.SAdd(TransactionKey, txHash.Hex()).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
		}
	}
	var logEntry []res.LogModel
	i := 0
	logCount := len(receipt.Logs)
	for _, receiptLog := range receipt.Logs {
		newLogEntry := res.LogModel{
			Address:                        receiptLog.Address.Hex(),
			BlockNumberANDTransactionIndex: blockNumberANDTransactionIndex,
			Data:                           fmt.Sprintf("%x", receiptLog.Data),
			TransactionHash:                TransactionHash,
			LogIndex:                       uint64(receiptLog.Index),
		}

		// 处理 Topics
		for j, topic := range receiptLog.Topics {
			if j >= 4 {
				break
			}
			topicHex := topic.Hex()
			switch j {
			case 0:
				newLogEntry.Topics0 = &topicHex
			case 1:
				newLogEntry.Topics1 = &topicHex
			case 2:
				newLogEntry.Topics2 = &topicHex
			case 3:
				newLogEntry.Topics3 = &topicHex
			}
		}

		logEntry = append(logEntry, newLogEntry)
		i++
		//判断log有没有获取完毕
		if uint(logCount) != receiptLog.Index+uint(1) {
			// 把 Hash 存到 redis
			err := global.Redis.SAdd(LogKey, txHash.Hex()).Err()
			if err != nil {
				fmt.Printf("Failed to add value to set: %v\n", err)
			}
		}
	}

	for _, entry := range logEntry {
		TransactionHash, err = models.InsertReceiptLog(global.DB, entry)
		if err != nil {
			err := global.Redis.SAdd(LogKey, txHash.Hex()).Err()
			if err != nil {
				fmt.Printf("Failed to add value to set: %v\n", err)
			}
		}
	}

}
