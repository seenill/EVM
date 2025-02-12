package global

import (
	"SeeEVM/config"
	"github.com/go-redis/redis"
	"gorm.io/gorm"
)

var (
	Config *config.Config //配置文件
	DB     *gorm.DB       //数据库
	Redis  *redis.Client
)
