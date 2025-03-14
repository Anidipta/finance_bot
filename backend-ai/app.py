from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder   
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage  
from langchain.agents import AgentExecutor, create_tool_calling_agent  
from langchain_core.output_parsers import StrOutputParser  
from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain_core.tools import tool, StructuredTool 
from google.cloud import firestore
from dotenv import load_dotenv  
from datetime import date
import yfinance as yf
import os

load_dotenv()

chat_history = []

if os.path.exists("chat_history.txt"):
    with open("chat_history.txt", "r") as file:
        for line in file.read().splitlines():
            if line.strip():
                chat_history.append(HumanMessage(content=line.strip()))


model = ChatGoogleGenerativeAI(
    model='gemini-1.5-pro',
    temperature=0.1,
    max_completion_tokens=100
)


db = firestore.Client()

classification_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a highly accurate AI assistant that classifies user queries based on intent who remembers chat history as well. Your primary task is to determine whether the query is seeking 'personalized advice', 'market data', or 'general information'. If the query is unrelated to these categories, politely inform the user that their question is off-topic. Remember, do not reveal internal processes or chain logic."
        ),
        
        MessagesPlaceholder(variable_name="chat_history"),
        
        (
            "user",
            "Classify the intent of this query into one of the following categories: 'personalized advice', 'market data', or 'general information'. \n Query: {query}"
        )
    ]
)

classification_chain = classification_template | model | StrOutputParser()

@tool
def company_information(ticker: str) -> dict:
    """Use this tool to retrieve company information like address, industry, sector, company officers, business summary, website, marketCap, current price, ebitda, total debt, total revenue, debt-to-equity, etc."""
    
    ticker_obj = yf.Ticker(ticker)
    ticker_info = ticker_obj.get_info()

    return ticker_info

@tool
def last_dividend_and_earnings_date(ticker: str) -> dict:
    """
    Use this tool to retrieve company's last dividend date and earnings release dates.
    It does not provide information about historical dividend yields.
    """
    ticker_obj = yf.Ticker(ticker)
    
    return ticker_obj.get_calendar()

@tool
def summary_of_mutual_fund_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top mutual fund holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)
    mf_holders = ticker_obj.get_mutualfund_holders()
    
    return mf_holders.to_dict(orient="records")

@tool
def summary_of_institutional_holders(ticker: str) -> dict:
    """
    Use this tool to retrieve company's top institutional holders. 
    It also returns their percentage of share, stock count and value of holdings.
    """
    ticker_obj = yf.Ticker(ticker)   
    inst_holders = ticker_obj.get_institutional_holders()
    
    return inst_holders.to_dict(orient="records")

@tool
def stock_grade_updrages_downgrades(ticker: str) -> dict:
    """
    Use this to retrieve grade ratings upgrades and downgrades details of particular stock.
    It'll provide name of firms along with 'To Grade' and 'From Grade' details. Grade date is also provided.
    """
    ticker_obj = yf.Ticker(ticker)
    
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
    ticker_obj = yf.Ticker(ticker)
    hist_splits = ticker_obj.get_splits()
    
    return hist_splits.to_dict()

@tool
def stock_news(ticker: str) -> dict:
    """
    Use this to retrieve latest news articles discussing particular stock ticker.
    """
    ticker_obj = yf.Ticker(ticker)
    
    return ticker_obj.get_news()

@tool
def stock_compare(ticker1: str, ticker2: str) -> dict:
    """
    Use this tool to compare two stock tickers.
    """
    ticker1_obj = yf.Ticker(ticker1)
    ticker2_obj = yf.Ticker(ticker2)
    print(ticker1_obj.info)
    return {
        ticker1: ticker1_obj.info,
        ticker2: ticker2_obj.info
    }

@tool
def last_n_years_dividends(ticker: str, n: int) -> dict:
    """
    Use this tool to retrieve last n years of dividends data.
    """
    ticker_obj = yf.Ticker(ticker)
    dividends = ticker_obj.dividends
    return dividends.tail(n).to_dict()


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

market_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly AI assistant. Your primary and only task is to answer {messages} using available tools. If a query is off-topic, you politely refuse without sharing any internal chain logic.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

market_finance_agent = create_tool_calling_agent(model, tools_for_market_agent, market_agent_prompt)
market_finance_agent_executor = AgentExecutor(agent=market_finance_agent, tools=tools_for_market_agent)

general_information_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly AI assistant. Your primary and only task is to provide general information or educational information based on the {input}. You serve as a generative AI that generates a response based on the user's query and the chat history. If a query is off-topic, you politely refuse without sharing any internal chain logic. If you don't know something just say it in a polite way. Don't provide wrong information or hallucinate."
        ),

        (
            "user",
            "I need some general educational information on {input}."
        )
    ]
)

general_chain = general_information_template | model | StrOutputParser()

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

def stock_performance_analysis(ticker: str, period: str = "1y") -> dict:
    """
    Analyze the historical performance of a stock over a specified period.
    Returns metrics such as average return, volatility, and trend direction.
    """
    ticker_obj = yf.Ticker(ticker)
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
    ticker_obj = yf.Ticker(ticker)
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
        ticker_obj = yf.Ticker(ticker)
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


personalized_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a versatile and intelligent AI assistant, designed to help the user in a personalized and friendly manner. You excel at answering {messages}, performing calculations, analyzing stock performance, fetching real-time information from various sources like Firestore, and providing localized insights. You always prioritize what benefits the user and can handle complex queries seamlessly. If a request is beyond your scope, you politely decline without revealing internal logic or processes. Don't hallucinate. If you don't know or can't do something, just tell it",
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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

personalized_finance_agent = create_tool_calling_agent(model, tools_for_market_agent, personalized_agent_prompt)
personalized_finance_agent_executor = AgentExecutor(agent=personalized_finance_agent, tools=tools_for_personalized_agent)

while True:
    user_query = input("You: ")
    if user_query.lower() == "exit":
        print("AI : Goodbye!")
        with open("chat_history.txt", "w") as file:
            for message in chat_history:
                file.write(message.content + "\n")
        break
    chat_history.append(HumanMessage(content=user_query))

    intent = classification_chain.invoke({"chat_history": chat_history, "query": user_query})
    print("Intent:", intent)
    
    branch_inputs = {
        "chat_history": chat_history,
        "intent": intent,
        "output": user_query  
    }
    if "Market" in branch_inputs.get("intent", ""):
        try:
            market_answer = market_finance_agent_executor.invoke({"messages": [HumanMessage(content=user_query)]})
            market_answer_content = market_answer.get("output", "Sorry, either corresponding data not found.")
        except Exception as e:
            market_answer_content = f"Sorry, there is either some problem while fetching the information or permit restricted"
        chat_history.append(AIMessage(content=market_answer_content))
        print("AI:", market_answer_content)

    elif "General" in branch_inputs.get("intent", ""):
        try:
            general_answer = general_chain.invoke({"input": [HumanMessage(content=user_query)]})
        except Exception as e:
            general_answer = f"Sorry, there is either some problem while fetching the information or permit restricted"
        chat_history.append(AIMessage(content=general_answer))
        print("AI:", general_answer)

    elif "Personalized" in branch_inputs.get("intent", ""):
        try:
            personalized_answer = personalized_finance_agent_executor.invoke({"messages": [HumanMessage(content=user_query)]})
            personalized_answer_content = personalized_answer.get("output", "Sorry, permission restricted.")
        except Exception as e:
            personalized_answer_content = f"Sorry, there is either some problem while fetching the information or permit restricted"
        chat_history.append(AIMessage(content=personalized_answer_content))
        print("AI:", personalized_answer_content)

    else:
            print("AI: I'm sorry, I'm not sure how to help with that. Please ask me something else.")

