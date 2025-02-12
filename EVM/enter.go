package EVM

import (
	"SeeEVM/global"
	"SeeEVM/models"
	"SeeEVM/models/res"
	"context"
	"fmt"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
	"log"
	"math/big"
	"strconv"
	"sync"
	"time"
)

func GetReceiptInfo() {
	//获取
	client, connected := ConnectToEthereum()
	if !connected {
		return
	}
	defer client.Close()

	latestBlockNumber, err := GetBlockNumber(client)
	if err != nil {
		log.Fatalf("无法获取最新区块编号: %v", err)
	}
	log.Printf("当前最新区块编号: %d", latestBlockNumber)
	processedBlockNumber := latestBlockNumber

	txHashChan := make(chan common.Hash)
	var wg sync.WaitGroup

	// 启动协程工作者
	for i := 0; i < PoolSize; i++ {
		wg.Add(1)
		go Worker(client, txHashChan, &wg)
	}

	ticker := time.NewTicker(time.Duration(CheckInterval) * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		newLatestBlockNumber, err := GetBlockNumber(client)
		if err != nil {
			log.Printf("获取最新区块编号时出错: %v", err)
			time.Sleep(time.Duration(ErrorRetryWait) * time.Second)
			continue
		}

		blockDifference := newLatestBlockNumber - processedBlockNumber
		if blockDifference > 0 {
			for blockNum := processedBlockNumber + 1; blockNum <= newLatestBlockNumber; blockNum++ {
				processBlock(client, blockNum, txHashChan)
			}
			processedBlockNumber = newLatestBlockNumber
		}
	}

	close(txHashChan)
	wg.Wait()
}

func processBlock(client *ethclient.Client, blockNumber uint64, txHashChan chan<- common.Hash) {
	log.Printf("正在处理区块 %d...", blockNumber)
	//获取区块
	block, err := client.BlockByNumber(context.Background(), big.NewInt(int64(blockNumber)))
	if err != nil {
		log.Printf("获取区块 %d 信息时出错: %v", strconv.FormatUint(blockNumber, 10), err)
		err := global.Redis.SAdd("block", strconv.FormatUint(blockNumber, 10)).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
			return
		}
		return
	}
	var blockStruct res.BlockModel
	// 从 block 对象中提取数据并赋值到 Block 结构体中
	blockStruct.VersionNumber = 0 // 以太坊区块没有直接的版本号，这里先设为 0
	blockStruct.PreviousBlockHash = block.ParentHash().Hex()
	blockStruct.MerkleRoot = block.TxHash().Hex()
	blockStruct.Timestamp = int(block.Time())
	blockStruct.DifficultyTarget = int(block.Difficulty().Int64())
	blockStruct.Nonce = int(block.Nonce())
	blockStruct.BlockHeight = uint64(block.Number().Int64())
	blockStruct.MinerAddress = block.Coinbase().Hex()
	blockStruct.Signature = "" // 以太坊区块没有直接的签名信息，这里先设为空
	blockStruct.PreviousBlockHash, err = models.InsertBlock(global.DB, blockStruct)
	if err != nil {
		//把PreviousBlockHash存入redis
		err := global.Redis.SAdd(BlockKey, strconv.FormatUint(blockNumber, 10)).Err()
		if err != nil {
			fmt.Printf("Failed to add value to set: %v\n", err)
			return
		}
	}

	for _, tx := range block.Transactions() {
		txHashChan <- tx.Hash()
	}
}
