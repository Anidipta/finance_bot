# @tool
# def get_current_price(ticker: str) -> dict:
#     """
#     Retrieve the current market price for the given ticker.
#     This uses the YFinance API to get the 'regularMarketPrice' from the ticker's info.
#     """
#     ticker_obj = Ticker(ticker)
#     info = ticker_obj.get_info()
#     current_price = info.get("regularMarketPrice")
#     if current_price is None:
#         return {"error": f"Current price not available for ticker {ticker}."}
#     return {"ticker": ticker, "current_price": current_price}

# @tool
# def company_information(ticker: str) -> dict:
#     """
#     Retrieve company information (address, industry, sector, officers,
#     business summary, website, market cap, etc.) for the given ticker.
#     """
#     ticker_obj = Ticker(ticker)
#     return ticker_obj.get_info()

# @tool
# def last_dividend_and_earnings_date(ticker: str) -> dict:
#     """
#     Retrieve the company's last dividend and earnings release dates.
#     """
#     ticker_obj = Ticker(ticker)
#     return ticker_obj.get_calendar()

# @tool
# def stock_splits_history(ticker: str) -> dict:
#     """
#     Retrieve historical stock splits data for the given ticker.
#     """
#     ticker_obj = Ticker(ticker)
#     splits = ticker_obj.get_splits()
#     return splits.to_dict()

# @tool
# def stock_news(ticker: str) -> dict:
#     """
#     Retrieve the latest news articles for the given stock ticker.
#     """
#     ticker_obj = Ticker(ticker)
#     return ticker_obj.get_news()

# @tool
# def stock_compare(ticker1: str, ticker2: str) -> dict:
#     """
#     Compare two stock tickers by returning their respective company information.
#     """
#     return {
#         ticker1: Ticker(ticker1).get_info(),
#         ticker2: Ticker(ticker2).get_info()
#     }

# @tool
# def last_n_years_dividends(ticker: str, n: int) -> dict:
#     """
#     Retrieve dividends data for the last n years for the given ticker.
#     """
#     ticker_obj = Ticker(ticker)
#     dividends = ticker_obj.dividends
#     return dividends.tail(n).to_dict()

# @tool
# def summary_of_mutual_fund_holders(ticker: str) -> dict:
#     """
#     Retrieve company's top mutual fund holders including percentage of share,
#     stock count, and value of holdings.
#     """
#     ticker_obj = Ticker(ticker)
#     mf_holders = ticker_obj.get_mutualfund_holders()
#     try:
#         # Convert dataframe to list of records (if available)
#         return mf_holders.to_dict(orient="records")
#     except Exception as e:
#         return {"error": str(e)}

# @tool
# def summary_of_institutional_holders(ticker: str) -> dict:
#     """
#     Retrieve company's top institutional holders including percentage of share,
#     stock count, and value of holdings.
#     """
#     ticker_obj = Ticker(ticker)
#     inst_holders = ticker_obj.get_institutional_holders()
#     try:
#         return inst_holders.to_dict(orient="records")
#     except Exception as e:
#         return {"error": str(e)}


# @tool
# def calculate_profit_loss(ticker: str, purchase_price: float, quantity: int, current_price: float) -> dict:
#     """
#     Calculate the profit or loss for a stock based on purchase price, quantity,
#     and current price. Returns both absolute and percentage changes.
#     """
#     profit_loss = (current_price - purchase_price) * quantity
#     total_investment = purchase_price * quantity
#     percentage_change = (profit_loss / total_investment) * 100 if total_investment else None
#     return {"profit_loss": profit_loss, "percentage_change": percentage_change}

# @tool
# def expected_return(ticker: str, purchase_price: float, quantity: int, target_price: float) -> dict:
#     """
#     Calculate the expected return for a stock based on purchase price, quantity,
#     and target price. Returns both absolute expected return and percentage change.
#     """
#     exp_return = (target_price - purchase_price) * quantity
#     percentage_change = ((target_price - purchase_price) / purchase_price) * 100 if purchase_price else None
#     return {"expected_return": exp_return, "percentage_change": percentage_change}

# @tool
# def stock_performance_analysis(ticker: str, period: str = "1y") -> dict:
#     """
#     Analyze historical performance of a stock over a specified period.
#     Returns average return, volatility, and trend direction.
#     """
#     ticker_obj = Ticker(ticker)
#     hist = ticker_obj.history(period=period)
#     if hist.empty:
#         return {"error": "No historical data available."}
#     avg_return = hist['Close'].pct_change().mean() * 100
#     volatility = hist['Close'].pct_change().std() * 100
#     trend = "upward" if hist['Close'].iloc[-1] > hist['Close'].iloc[0] else "downward"
#     return {"average_return": avg_return, "volatility": volatility, "trend": trend}

# @tool
# def buy_sell_recommendation(ticker: str) -> dict:
#     """
#     Provide a simple recommendation to buy or sell a stock using a moving
#     average crossover strategy.
#     """
#     ticker_obj = Ticker(ticker)
#     hist = ticker_obj.history(period="6mo")
#     if hist.empty:
#         return {"error": "No historical data available."}
#     short_ma = hist['Close'].rolling(window=20).mean().iloc[-1]
#     long_ma = hist['Close'].rolling(window=50).mean().iloc[-1]
#     recommendation = "buy" if short_ma > long_ma else "sell"
#     return {"short_moving_average": short_ma, "long_moving_average": long_ma, "recommendation": recommendation}

# @tool
# def get_user_portfolio(user_id: str) -> dict:
#     """
#     Retrieve the user's portfolio from the stocks collection.
#     The collection follows the schema:
#       { userId: <ObjectId>, stocks: [ { stock: <String>, holding: <Number> } ] }
#     """
#     portfolio = stocks_collection.find_one({"userId": user_id})
#     if portfolio:
#         return portfolio
#     return {"error": "No portfolio found for user."}

# @tool
# def add_stock(user_id: str, stock: str, holding: int) -> Dict[str, Any]:
#     """
#     Add a stock to a user's portfolio.
#     """
#     result = stocks_collection.update_one(
#         {"userId": user_id},
#         {"$push": {"stocks": {"stock": stock, "holding": holding}}},
#         upsert=True  # In case no document exists for the user, create one.
#     )
#     if result.modified_count or result.upserted_id:
#         return {"message": f"Added {stock} ({holding} shares) for user {user_id}."}
#     return {"error": "Failed to add stock."}

# @tool
# def edit_stock(user_id: str, stock: str, new_holding: int) -> Dict[str, Any]:
#     """
#     Update the holding quantity of a stock in a user's portfolio.
#     """
#     result = stocks_collection.update_one(
#         {"userId": user_id, "stocks.stock": stock},
#         {"$set": {"stocks.$.holding": new_holding}}
#     )
#     if result.matched_count == 0:
#         return {"message": f"Stock {stock} not found for user {user_id}."}
#     return {"message": f"Updated {stock} holding to {new_holding} shares for user {user_id}."}

# @tool
# def delete_stock(user_id: str, stock: str) -> Dict[str, Any]:
#     """
#     Delete a stock from a user's portfolio.
#     """
#     result = stocks_collection.update_one(
#         {"userId": user_id},
#         {"$pull": {"stocks": {"stock": stock}}}
#     )
#     if result.modified_count == 0:
#         return {"message": f"Stock {stock} not found for user {user_id}."}
#     return {"message": f"Deleted {stock} from user {user_id}."}

# @tool
# def aggregate_market_data(tickers: list[str]) -> dict:
#     """
#     Retrieve and aggregate market data for multiple tickers.
#     Returns a summary including average price and total market capitalization.
#     """
#     aggregated = {}
#     total_price = 0
#     count = 0
#     market_caps = []
#     for ticker in tickers:
#         info = Ticker(ticker).get_info()
#         price = info.get("regularMarketPrice")
#         market_cap = info.get("marketCap")
#         aggregated[ticker] = {"price": price, "marketCap": market_cap}
#         if price is not None:
#             total_price += price
#             count += 1
#         if market_cap is not None:
#             market_caps.append(market_cap)
#     avg_price = total_price / count if count > 0 else None
#     total_market_cap = sum(market_caps) if market_caps else None
#     aggregated["summary"] = {"average_price": avg_price, "total_market_cap": total_market_cap}
#     return aggregated

# tools_for_market_agent = [
#     get_current_price,
#     company_information,
#     last_dividend_and_earnings_date,
#     stock_splits_history,
#     stock_news,
#     stock_compare,
#     last_n_years_dividends,
#     summary_of_mutual_fund_holders,
#     summary_of_institutional_holders
# ]

# tools_for_personalized_agent = [
#     company_information,
#     calculate_profit_loss,
#     expected_return,
#     stock_performance_analysis,
#     buy_sell_recommendation,
#     get_user_portfolio,
#     add_stock,
#     delete_stock,
#     edit_stock,
#     aggregate_market_data
# ]

import os
from langchain.tools import tool
from yfinance import Ticker
from datetime import date
from typing import Dict, Any, List
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set in the environment variables.")

client = MongoClient(MONGODB_URL)
db = client["test"]
stocks_collection = db["stocks"]


@tool
def get_current_price(ticker: str) -> dict:
    """
    Retrieve the current market price for the given ticker.
    This uses the YFinance API to get the 'regularMarketPrice' from the ticker's info.
    """
    ticker_obj = Ticker(ticker)
    info = ticker_obj.get_info()
    current_price = info.get("regularMarketPrice")
    if current_price is None:
        return {"error": f"Current price not available for ticker {ticker}."}
    return {"ticker": ticker, "current_price": current_price}

@tool
def company_information(ticker: str) -> dict:
    """
    Retrieve company information (address, industry, sector, officers,
    business summary, website, market cap, etc.) for the given ticker.
    """
    ticker_obj = Ticker(ticker)
    return ticker_obj.get_info()

@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """
    Retrieve the company's last dividend and earnings release dates.
    """
    ticker_obj = Ticker(ticker)
    return ticker_obj.get_calendar()

@tool
def stock_splits_history(ticker: str) -> dict:
    """
    Retrieve historical stock splits data for the given ticker.
    """
    ticker_obj = Ticker(ticker)
    splits = ticker_obj.get_splits()
    return splits.to_dict()

@tool
def stock_news(ticker: str) -> dict:
    """
    Retrieve the latest news articles for the given stock ticker.
    """
    ticker_obj = Ticker(ticker)
    return ticker_obj.get_news()

@tool
def stock_compare(ticker1: str, ticker2: str) -> dict:
    """
    Compare two stock tickers by returning their respective company information.
    """
    return {
        ticker1: Ticker(ticker1).get_info(),
        ticker2: Ticker(ticker2).get_info()
    }

@tool
def last_n_years_dividends(ticker: str, n: int) -> dict:
    """
    Retrieve dividends data for the last n years for the given ticker.
    """
    ticker_obj = Ticker(ticker)
    dividends = ticker_obj.dividends
    return dividends.tail(n).to_dict()

@tool
def summary_of_mutual_fund_holders(ticker: str) -> dict:
    """
    Retrieve company's top mutual fund holders including percentage of share,
    stock count, and value of holdings.
    """
    ticker_obj = Ticker(ticker)
    mf_holders = ticker_obj.get_mutualfund_holders()
    try:
        return mf_holders.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@tool
def summary_of_institutional_holders(ticker: str) -> dict:
    """
    Retrieve company's top institutional holders including percentage of share,
    stock count, and value of holdings.
    """
    ticker_obj = Ticker(ticker)
    inst_holders = ticker_obj.get_institutional_holders()
    try:
        return inst_holders.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@tool
def calculate_profit_loss(ticker: str, purchase_price: float, quantity: int, current_price: float) -> dict:
    """
    Calculate the profit or loss for a stock based on purchase price, quantity,
    and current price. Returns both absolute and percentage changes.
    """
    profit_loss = (current_price - purchase_price) * quantity
    total_investment = purchase_price * quantity
    percentage_change = (profit_loss / total_investment) * 100 if total_investment else None
    return {"profit_loss": profit_loss, "percentage_change": percentage_change}

@tool
def expected_return(ticker: str, purchase_price: float, quantity: int, target_price: float) -> dict:
    """
    Calculate the expected return for a stock based on purchase price, quantity,
    and target price. Returns both absolute expected return and percentage change.
    """
    exp_return = (target_price - purchase_price) * quantity
    percentage_change = ((target_price - purchase_price) / purchase_price) * 100 if purchase_price else None
    return {"expected_return": exp_return, "percentage_change": percentage_change}

@tool
def stock_performance_analysis(ticker: str, period: str = "1y") -> dict:
    """
    Analyze historical performance of a stock over a specified period.
    Returns average return, volatility, and trend direction.
    """
    ticker_obj = Ticker(ticker)
    hist = ticker_obj.history(period=period)
    if hist.empty:
        return {"error": "No historical data available."}
    avg_return = hist['Close'].pct_change().mean() * 100
    volatility = hist['Close'].pct_change().std() * 100
    trend = "upward" if hist['Close'].iloc[-1] > hist['Close'].iloc[0] else "downward"
    return {"average_return": avg_return, "volatility": volatility, "trend": trend}

@tool
def buy_sell_recommendation(ticker: str) -> dict:
    """
    Provide a simple recommendation to buy or sell a stock using a moving
    average crossover strategy.
    """
    ticker_obj = Ticker(ticker)
    hist = ticker_obj.history(period="6mo")
    if hist.empty:
        return {"error": "No historical data available."}
    short_ma = hist['Close'].rolling(window=20).mean().iloc[-1]
    long_ma = hist['Close'].rolling(window=50).mean().iloc[-1]
    recommendation = "buy" if short_ma > long_ma else "sell"
    return {"short_moving_average": short_ma, "long_moving_average": long_ma, "recommendation": recommendation}

@tool
def get_user_portfolio(user_id: str) -> Dict[str, Any]:
    """
    Retrieve the user's portfolio from the stocks collection.
    Tries both string and ObjectId lookups for flexibility.
    The collection schema:
      { userId: <ObjectId or String>, stocks: [ { stock: <String>, holding: <Number> } ] }
    """
    try:
        portfolio = stocks_collection.find_one({"userId": user_id})
        if not portfolio:
            try:
                object_id = ObjectId(user_id)
                portfolio = stocks_collection.find_one({"userId": object_id})
            except Exception:
                pass

        if portfolio:
            return {
                "userId": str(portfolio.get("userId") or portfolio.get("user_id")),
                "stocks": portfolio.get("stocks", [])
            }

        return {"error": f"No portfolio found for user {user_id}. Please check the user ID is correct."}
    
    except Exception as e:
        return {"error": f"Error retrieving portfolio: {str(e)}"}

@tool
def add_stock(user_id: str, stock: str, holding: int) -> Dict[str, Any]:
    """
    Add a stock to a user's portfolio.
    """
    result = stocks_collection.update_one(
        {"userId": user_id},
        {"$push": {"stocks": {"stock": stock, "holding": holding}}},
        upsert=True  
    )
    if result.modified_count or result.upserted_id:
        return {"message": f"Added {stock} ({holding} shares) for user {user_id}."}
    return {"error": "Failed to add stock."}

# @tool
# def edit_stock(user_id: str, stock: str, new_holding: int) -> Dict[str, Any]:
#     """
#     Update the holding quantity of a stock in a user's portfolio.
#     """
#     result = stocks_collection.update_one(
#         {"userId": user_id, "stocks.stock": stock},
#         {"$set": {"stocks.$.holding": new_holding}}
#     )
#     if result.matched_count == 0:
#         return {"message": f"Stock {stock} not found for user {user_id}."}
#     return {"message": f"Updated {stock} holding to {new_holding} shares for user {user_id}."}

@tool
def delete_stock(user_id: str, stock: str) -> Dict[str, Any]:
    """
    Delete a stock from a user's portfolio.
    """
    result = stocks_collection.update_one(
        {"userId": user_id},
        {"$pull": {"stocks": {"stock": stock}}}
    )
    if result.modified_count == 0:
        return {"message": f"Stock {stock} not found for user {user_id}."}
    return {"message": f"Deleted {stock} from user {user_id}."}

@tool
def aggregate_market_data(tickers: List[str]) -> dict:
    """
    Retrieve and aggregate market data for multiple tickers.
    Returns a summary including average price and total market capitalization.
    """
    aggregated = {}
    total_price = 0
    count = 0
    market_caps = []
    for ticker in tickers:
        info = Ticker(ticker).get_info()
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
    get_current_price,
    company_information,
    last_dividend_and_earnings_date,
    stock_splits_history,
    stock_news,
    stock_compare,
    last_n_years_dividends,
    summary_of_mutual_fund_holders,
    summary_of_institutional_holders
]

tools_for_personalized_agent = [
    company_information,
    calculate_profit_loss,
    expected_return,
    stock_performance_analysis,
    buy_sell_recommendation,
    get_user_portfolio,
    add_stock,
    delete_stock,
    #edit_stock,
    aggregate_market_data
]