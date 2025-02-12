package initialize

import (
	"SeeEVM/global"
	"fmt"
	"gopkg.in/yaml.v3"
	"io/ioutil"
)

func InitConfig() error {
	yamlFile, err := ioutil.ReadFile("config.yaml")
	if err != nil {
		fmt.Printf("Error reading YAML file: %v\n", err)
		return err
	}
	// 解析YAML数据到Config结构体
	err = yaml.Unmarshal(yamlFile, &global.Config)
	if err != nil {
		fmt.Printf("Error unmarshaling YAML data: %v\n", err)
		return err
	}
	return nil
}
