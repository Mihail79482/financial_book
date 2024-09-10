import requests
import logging
from db import save_raw_data

def fetch_btc_data(symbol, tsym='USD', limit=30, toTs=None):
    """从 CryptoCompare API 获取指定币种的数据"""
    api_url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': symbol,
        'tsym': tsym,
        'limit': limit,  # 获取 limit 天的数据
        'aggregate': 1,
        'e': 'CCCAGG',
        'toTs': toTs
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()['Data']['Data']

        # 为每个数据条目添加币种字段
        for entry in data:
            entry['symbol'] = symbol

        logging.info(f"Fetched {len(data)} days of {symbol}/{tsym} data.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {symbol}/{tsym} data: {e}")
        return None

def store_data_in_db(data):
    """将数据存储到数据库，包含币种字段"""
    save_raw_data(data)
    logging.info(f"Stored {len(data)} records to the database.")
