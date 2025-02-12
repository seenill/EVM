package main

import (
	"SeeEVM/EVM"
	"SeeEVM/global"
	"SeeEVM/initialize"
)

func main() {
	//读取配置文件逻辑
	err := initialize.InitConfig()
	//对数据库等初始化
	global.DB, err = initialize.InitMysql()
	if err != nil {
		return
	}
	//redis初始化
	global.Redis = initialize.InitRedis()
	if global.Redis == nil {
		return
	}
	//获取链上数据
	EVM.GetReceiptInfo()
}
