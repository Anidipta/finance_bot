import os
import yfinance as yf
from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime
import threading
import time

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

current_symbol = "NVDA"
monitoring_thread = None
monitoring_lock = threading.Lock()

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo", interval="1d")
    if data.empty:
        return None

    ohlc_data = []
    for date, row in data.iterrows():
        ohlc_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        })

    return {
        "symbol": symbol.upper(),
        "data": ohlc_data,
        "timestamp": datetime.now().isoformat()
    }

def start_stock_monitoring(interval=30):
    global current_symbol
    while True:
        result = fetch_stock_data(current_symbol)
        if result:
            socketio.emit('stock_update', result)
        time.sleep(interval)

@socketio.on('start_monitoring')
def handle_start_monitoring(data):
    global current_symbol, monitoring_thread
    symbol = data.get('symbol', 'NVDA').upper()
    interval = data.get('interval', 30)

    with monitoring_lock:
        current_symbol = symbol
        if monitoring_thread is None or not monitoring_thread.is_alive():
            monitoring_thread = threading.Thread(
                target=start_stock_monitoring,
                args=(interval,),
                daemon=True
            )
            monitoring_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)