from fastapi import FastAPI
from yfinance import Ticker
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

@app.get("/stock/{symbol}", response_model=List[StockData])
def get_stock_data(symbol: str, period: str = "1mo", interval: str = "1d"):
    stock = Ticker(symbol)
    data = stock.history(period=period, interval=interval)
    
    if data.empty:
        return []
    
    # Convert DataFrame to list of dictionaries
    stock_data = [
        {
            "date": index.strftime("%Y-%m-%d %H:%M:%S"),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        }
        for index, row in data.iterrows()
    ]
    return stock_data