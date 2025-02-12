package config

type MySQL struct {
	User   string `yaml:"user"`
	Pass   string `yaml:"pass"`
	Host   string `yaml:"host"`
	Port   string `yaml:"port"`
	DbName string `yaml:"dbname"`
}
type Redis struct {
	Addr     string `yaml:"addr"`
	Password string `yaml:"password"`
	DB       int    `yaml:"db"`
}
type Config struct {
	Mysql MySQL `yaml:"mysql"`

	Redis Redis `yaml:"redis"`
}
