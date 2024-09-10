from pymongo import MongoClient
import logging

# 连接 MongoDB
client = MongoClient("mongodb://172.19.160.1:27017/")
db = client['btc_data']  # 数据库名
raw_data_collection = db['raw_btc_data']  # 集合名

def save_raw_data(data):
    try:
        # 插入文档到 MongoDB
        result = raw_data_collection.insert_many(data)
        logging.info(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
    except Exception as e:
        logging.error(f"Error saving data to MongoDB: {e}")
