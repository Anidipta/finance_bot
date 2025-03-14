import plotly.graph_objects as go
from yfinance import Ticker
import pandas as pd

def plot_stock_price(symbol="NVDA", period="1mo", interval="1d", margin=0.02):
    stock = Ticker(symbol)
    data = stock.history(period=period, interval=interval)
    
    if data.empty:
        print("No data available.")
        return
    
    data['Color'] = data['Close'].diff().apply(lambda x: 'green' if x > 0 else 'red')
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='limegreen',
        decreasing_line_color='crimson',
        name='Candlestick'
    ))
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Close'].diff(),
        marker=dict(color=data['Color']),
        opacity=0.7,
        name='Daily Change'
    ))
    
    min_price = data['Low'].min() * (1 - margin)
    max_price = data['High'].max() * (1 + margin)
    
    fig.add_trace(go.Scatter(
        x=[data.index[0], data.index[-1]],
        y=[min_price, max_price],
        mode='lines',
        line=dict(color='blue', width=2, dash='dash'),
        name='Margin'
    ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price Over Time',
        template='plotly_dark',
        yaxis=dict(title='Price', range=[min_price, max_price]),
        xaxis=dict(title='Date'),
        plot_bgcolor='black',
        paper_bgcolor='black'
    )
    
    fig.show()

