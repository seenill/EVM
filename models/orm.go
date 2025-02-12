package models

import (
	"SeeEVM/models/res"
	"gorm.io/gorm"
)

// Receipt
func InsertReceipt(db *gorm.DB, model res.ReceiptModel) (string, error) {
	DB := db.Create(&model)
	if DB.Error != nil {
		return model.TransactionHash, DB.Error
	}
	return "", nil
}

//Transaction

func InsertTransaction(db *gorm.DB, model res.TransactionModel) (string, error) {
	DB := db.Create(&model)
	if DB.Error != nil {
		return model.Hash, DB.Error
	}
	return "", nil
}

// log
func InsertReceiptLog(db *gorm.DB, model res.LogModel) (string, error) {
	DB := db.Create(&model)
	if DB.Error != nil {
		return model.TransactionHash, DB.Error
	}
	return "", nil
}

func InsertBlock(db *gorm.DB, model res.BlockModel) (string, error) {
	DB := db.Create(&model)
	if DB.Error != nil {
		return model.PreviousBlockHash, DB.Error
	}
	return "", nil
}
