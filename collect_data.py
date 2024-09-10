import argparse
import time
import logging
from data_collector import fetch_btc_data, store_data_in_db
import os

# 配置日志
logging.basicConfig(filename='logs/data_collection.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

LAST_TS_FILE = 'last_ts.txt'  # 用来记录上一次成功执行的时间戳

def read_last_ts():
    """读取上一次成功请求的时间戳"""
    if os.path.exists(LAST_TS_FILE):
        with open(LAST_TS_FILE, 'r') as f:
            return int(f.read().strip())
    return None

def write_last_ts(toTs):
    """记录当前成功请求的时间戳"""
    with open(LAST_TS_FILE, 'w') as f:
        f.write(str(toTs))

def collect_data(symbol, tsym, interval, limit, retries=3, single_run=False):
    """根据给定的参数获取数据并存储，支持单次执行或自动向前获取更多数据"""
    toTs = read_last_ts()  # 读取上次的时间戳，若无则为 None，获取最新数据

    while True:
        try:
            logging.info(f"Fetching data for {symbol}/{tsym} with limit {limit} and toTs {toTs}")
            
            # 每次请求之前详细记录请求参数
            logging.info(f"Request Params: symbol={symbol}, tsym={tsym}, limit={limit}, toTs={toTs}")

            data = fetch_btc_data(symbol, tsym, limit=limit, toTs=toTs)

            if not data:
                logging.info(f"No more data for {symbol}/{tsym}. Stopping collection.")
                break

            store_data_in_db(data)  # 存储到数据库
            logging.info(f"Successfully stored {len(data)} records for {symbol}/{tsym}.")

            # 获取更早的数据
            toTs = data[0]['time']  # 设置为获取到数据的最早时间
            write_last_ts(toTs)  # 每次成功请求后记录当前时间戳

            if single_run:  # 如果只执行一次则退出循环
                logging.info("Single run complete. Exiting.")
                break

            time.sleep(interval)  # 等待 interval 秒
        except Exception as e:
            # 记录失败的请求和参数
            logging.error(f"Error fetching data for {symbol}/{tsym} with limit {limit} and toTs {toTs}: {e}")
            if retries > 0:
                logging.info(f"Retrying... ({retries} retries left)")
                retries -= 1
                time.sleep(interval)
            else:
                logging.error(f"Failed after multiple retries for {symbol}/{tsym} with toTs {toTs}. Exiting.")
                break

if __name__ == '__main__':
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Collect cryptocurrency data.')
    parser.add_argument('--symbol', type=str, required=True, help='The symbol of the cryptocurrency to fetch, e.g., BTC.')
    parser.add_argument('--tsym', type=str, default='USD', help='The target currency symbol, e.g., USD.')
    parser.add_argument('--interval', type=int, default=5, help='Interval between requests in seconds.')
    parser.add_argument('--limit', type=int, default=30, help='Number of data points per request.')
    parser.add_argument('--retries', type=int, default=3, help='Number of retries if a request fails.')
    parser.add_argument('--single', action='store_true', help='Run a single data collection without fetching more data.')
    
    args = parser.parse_args()

    # 执行数据收集
    collect_data(args.symbol, args.tsym, args.interval, args.limit, args.retries, args.single)
