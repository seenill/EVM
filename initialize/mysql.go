package initialize

import (
	"SeeEVM/config"
	"SeeEVM/global"
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func InitMysql() (*gorm.DB, error) {
	// 定义 MySQL 连接参数
	//后续从环境变量读取
	mysqlConfig := config.MySQL{
		User:   global.Config.Mysql.User,
		Pass:   global.Config.Mysql.Pass,
		Host:   global.Config.Mysql.Host,
		Port:   global.Config.Mysql.Port,
		DbName: global.Config.Mysql.DbName,
	}

	// 拼接 MySQL 连接字符串
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		mysqlConfig.User, mysqlConfig.Pass, mysqlConfig.Host, mysqlConfig.Port, mysqlConfig.DbName)

	// 使用 GORM 连接到 MySQL 数据库
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		fmt.Printf("Failed to connect to MySQL database: %v\n", err)
		return nil, err
	}
	fmt.Println("Successfully connected to MySQL database")

	return db, nil
}
