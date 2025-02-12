package EVM

import (
	"context"
	"log"

	"github.com/ethereum/go-ethereum/ethclient"
)

// ConnectToEthereum 连接到以太坊节点
func ConnectToEthereum() (*ethclient.Client, bool) {
	client, err := ethclient.Dial(InfuraURL)
	if err != nil {
		log.Println("无法连接到以太坊节点，请检查网络或节点配置。")
		return nil, false
	}
	log.Println("已成功连接到以太坊节点。")
	return client, true
}

// GetBlockNumber 获取当前最新区块编号
func GetBlockNumber(client *ethclient.Client) (uint64, error) {
	return client.BlockNumber(context.Background())
}
