package EVM

import (
	"sync"
	"time"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
)

// Worker 协程工作者，从队列中取出任务并执行
func Worker(client *ethclient.Client, txHashChan <-chan common.Hash, wg *sync.WaitGroup) {
	defer wg.Done() //-1
	for txHash := range txHashChan {
		time.Sleep(100 * time.Millisecond) // 增加 100 毫秒的延迟
		ProcessTransactionLogs(client, txHash)
	}
}
