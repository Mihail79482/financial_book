from flask import Flask
# from scheduler import start_scheduler

app = Flask(__name__)

@app.route('/')
def index():
    return "Bitcoin Data Collector is Running!"

if __name__ == '__main__':
    # 启动 APScheduler
    # start_scheduler()
    app.run(host='0.0.0.0', port=5000)
