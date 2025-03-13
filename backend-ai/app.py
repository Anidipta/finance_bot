from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder   # type: ignore
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage  # type: ignore
from langchain.agents import AgentExecutor, create_tool_calling_agent  # type: ignore
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
from langchain_core.tools import tool, StructuredTool  # type: ignore
# from langchain.schema.runnable import RunnableBranch
from dotenv import load_dotenv  # type: ignore
from datetime import date
import yfinance as yf # type: ignore
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

# @tool
# def calculate_profit_loss(ticker: str, purchase_price: float, quantity: int, current_price: float) -> dict:
#     """
#     Use this tool to calculate profit or loss on a particular stock.
#     """
#     profit_loss = (current_price - purchase_price) * quantity
#     return {
#         "profit_loss": profit_loss,
#         "percentage_change": (profit_loss / (purchase_price * quantity)) * 100
#     }

# @tool
# def expected_return(ticker: str, purchase_price: float, quantity: int, target_price: float) -> dict:
#     """
#     Use this tool to calculate expected return on a particular stock.
#     """
#     return {
#         "expected_return": (target_price - purchase_price) * quantity,
#         "percentage_change": ((target_price - purchase_price) / purchase_price) * 100
#     }

# personalized_advice_template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful and friendly AI assistant. Your primary and only task is to provide personalized advice based on the {output}. You serve as a generative AI that generates a response based on the user's query and the chat history. If a query is off-topic, you politely refuse without sharing any internal chain logic."
#         ),
        
#         (
#             "user",
#             "I need some personalized advice on {output}."
#         )
#     ]
# )

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


tools = [
    company_information,
    last_dividend_and_earnings_date,
    stock_splits_history,
    summary_of_mutual_fund_holders,
    summary_of_institutional_holders, 
    stock_grade_updrages_downgrades,
    stock_news,
    stock_compare,
    # calculate_profit_loss,
    # expected_return,
    last_n_years_dividends
]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly AI assistant. Your primary and only task is to answer {messages} using available tools. If a query is off-topic, you politely refuse without sharing any internal chain logic.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

finance_agent = create_tool_calling_agent(model, tools, agent_prompt)
finance_agent_executor = AgentExecutor(agent=finance_agent, tools=tools)

# branches = RunnableBranch(
#     (
#         lambda inputs: "personalized" in inputs.get("intent", ""),
#         personalized_advice_template | model | StrOutputParser()
#     ),

#     (
#         lambda inputs: "market" in inputs.get("intent", ""),
#         finance_agent_executor
#     ),

#     general_information_template | model | StrOutputParser()
# )

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
        answer = finance_agent_executor.invoke({"messages": [HumanMessage(content=user_query)]})
        answer_content = answer.get("output", "Sorry, either corresponding data not found or permission restricted.")
        chat_history.append(AIMessage(content=answer_content))
        print("AI:", answer_content)

    elif "General" in branch_inputs.get("intent", ""):
        general_chain = general_information_template | model | StrOutputParser()
        answer = general_chain.invoke({"input": [HumanMessage(content=user_query)]})
        chat_history.append(AIMessage(content=answer))
        print("AI:", answer)

    else:
        print("AI: I'm sorry, I'm not sure how to help with that. Please ask me something else.")

