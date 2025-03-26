import sys
import os

# Add the parent directory to sys.path to make absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.agents import tool
from yfinance import Ticker
from typing import Dict, List, Any
from datetime import date

@tool
def company_information(ticker: str) -> dict:
    """Use this tool to retrieve company information like address, industry, sector, company officers, business summary, website, marketCap, current price, ebitda, total debt, total revenue, debt-to-equity, etc."""
    ticker_obj = Ticker(ticker)
    ticker_info = ticker_obj.get_info()
    return ticker_info

@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """
    Use this tool to retrieve company's last dividend date and earnings release dates.
    It does not provide information about historical dividend yields.
    """
    ticker_obj = Ticker(ticker)
    return ticker_obj.get_calendar()

@tool
def summary_of_mutual_fund_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top mutual fund holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = Ticker(ticker)
    mf_holders = ticker_obj.get_mutualfund_holders()
    return mf_holders.to_dict(orient="records")

@tool
def summary_of_institutional_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top institutional holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = Ticker(ticker)   
    inst_holders = ticker_obj.get_institutional_holders()
    return inst_holders.to_dict(orient="records")

@tool
def stock_grade_updrages_downgrades(ticker: str) -> dict:
    """
    Use this to retrieve grade ratings upgrades and downgrades details of particular stock.
    It'll provide name of firms along with 'To Grade' and 'From Grade' details. Grade date is also provided.
    """
    ticker_obj = Ticker(ticker)
    curr_year = date.today().year
    upgrades_downgrades = ticker_obj.get_upgrades_downgrades()
    upgrades_downgrades = upgrades_downgrades.loc[upgrades_downgrades.index > f"{curr_year}-01-01"]
    upgrades_downgrades = upgrades_downgrades[upgrades_downgrades["Action"].isin(["up", "down"])]
    return upgrades_downgrades.to_dict(orient="records")

@tool
def stock_splits_history(ticker: str) -> dict:
    """
    Use this tool to retrieve company's historical stock splits data.
    """
    ticker_obj = Ticker(ticker)
    hist_splits = ticker_obj.get_splits()
    return hist_splits.to_dict()

@tool
def stock_news(ticker: str) -> dict:
    """
    Use this to retrieve latest news articles discussing particular stock ticker.
    """
    ticker_obj = Ticker(ticker)
    return ticker_obj.get_news()

@tool
def stock_compare(ticker1: str, ticker2: str) -> dict:
    """
    Use this tool to compare two stock tickers.
    """
    ticker1_obj = Ticker(ticker1)
    ticker2_obj = Ticker(ticker2)
    return {
        ticker1: ticker1_obj.info,
        ticker2: ticker2_obj.info
    }

@tool
def last_n_years_dividends(ticker: str, n: int) -> dict:
    """
    Use this tool to retrieve last n years of dividends data.
    """
    ticker_obj = Ticker(ticker)
    dividends = ticker_obj.dividends
    return dividends.tail(n).to_dict()

@tool
def calculate_profit_loss(ticker: str, purchase_price: float, quantity: int, current_price: float) -> dict:
    """
    Calculate the profit or loss for a given stock based on purchase price, quantity, and current price.
    Returns both the absolute profit/loss and the percentage change.
    """
    profit_loss = (current_price - purchase_price) * quantity
    total_investment = purchase_price * quantity
    percentage_change = (profit_loss / total_investment) * 100 if total_investment != 0 else None
    return {
        "profit_loss": profit_loss,
        "percentage_change": percentage_change
    }

@tool
def expected_return(ticker: str, purchase_price: float, quantity: int, target_price: float) -> dict:
    """
    Calculate the expected return for a given stock based on purchase price, quantity, and target price.
    Returns both the absolute expected return and the percentage change.
    """
    expected_return_value = (target_price - purchase_price) * quantity
    percentage_change = ((target_price - purchase_price) / purchase_price) * 100 if purchase_price != 0 else None
    return {
        "expected_return": expected_return_value,
        "percentage_change": percentage_change
    }

@tool
def stock_performance_analysis(ticker: str, period: str = "1y") -> dict:
    """
    Analyze the historical performance of a stock over a specified period.
    Returns metrics such as average return, volatility, and trend direction.
    """
    ticker_obj = Ticker(ticker)
    hist = ticker_obj.history(period=period)
    if hist.empty:
        return {"error": "No historical data available."}
    avg_return = hist['Close'].pct_change().mean() * 100
    volatility = hist['Close'].pct_change().std() * 100
    trend = "upward" if hist['Close'][-1] > hist['Close'][0] else "downward"
    return {
        "average_return": avg_return,
        "volatility": volatility,
        "trend": trend
    }

@tool
def buy_sell_recommendation(ticker: str) -> dict:
    """
    Provide a basic recommendation on whether to buy or sell a stock using a moving average crossover strategy.
    Compares the short-term and long-term moving averages to generate a recommendation.
    """
    ticker_obj = Ticker(ticker)
    hist = ticker_obj.history(period="6mo")
    if hist.empty:
        return {"error": "No historical data available."}
    short_ma = hist['Close'].rolling(window=20).mean().iloc[-1]
    long_ma = hist['Close'].rolling(window=50).mean().iloc[-1]
    recommendation = "buy" if short_ma > long_ma else "sell"
    return {
        "short_moving_average": short_ma,
        "long_moving_average": long_ma,
        "recommendation": recommendation
    }

@tool
def get_user_portfolio(user_id: str) -> dict:
    """
    Retrieve the user's portfolio from Firestore.
    This returns details such as owned stocks, quantities, purchase prices, etc.
    """
    try:
        doc_ref = db.collection("portfolios").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {"error": "No portfolio found for user."}
    except Exception as e:
        return {"error": str(e)}

@tool
def aggregate_market_data(tickers: list) -> dict:
    """
    Retrieve and aggregate market data for multiple stock tickers.
    Returns a summary including average price and total market capitalization.
    """
    aggregated = {}
    total_price = 0
    count = 0
    market_caps = []
    for ticker in tickers:
        ticker_obj = Ticker(ticker)
        info = ticker_obj.info
        price = info.get("regularMarketPrice")
        market_cap = info.get("marketCap")
        aggregated[ticker] = {"price": price, "marketCap": market_cap}
        if price is not None:
            total_price += price
            count += 1
        if market_cap is not None:
            market_caps.append(market_cap)
    avg_price = total_price / count if count > 0 else None
    total_market_cap = sum(market_caps) if market_caps else None
    aggregated["summary"] = {"average_price": avg_price, "total_market_cap": total_market_cap}
    return aggregated

tools_for_market_agent = [
    company_information,
    last_dividend_and_earnings_date,
    stock_splits_history,
    summary_of_mutual_fund_holders,
    summary_of_institutional_holders,
    stock_grade_updrages_downgrades,
    stock_news,
    stock_compare,
    last_n_years_dividends
]

tools_for_personalized_agent = [
    company_information,
    last_dividend_and_earnings_date,
    stock_splits_history,
    summary_of_mutual_fund_holders,
    summary_of_institutional_holders,
    stock_grade_updrages_downgrades,
    stock_news,
    stock_compare,
    calculate_profit_loss,
    expected_return,
    last_n_years_dividends,
    stock_performance_analysis,
    buy_sell_recommendation,
    get_user_portfolio,
    aggregate_market_data
]
