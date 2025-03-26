import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Import tools 
from tools import *

# Initialize Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAREm6mv3oEAwfldsZpoag6QHoH90w8gaY"

# Initialize Google Generative AI Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    max_output_tokens=300
)
# Classification Chain
classification_template = ChatPromptTemplate.from_messages([
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

# Market Finance Agent
market_agent_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are an AI assistant for market finance queries. "
        "Use available tools to provide accurate market information."
    ),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

market_finance_agent = create_tool_calling_agent(
    model, 
    tools_for_market_agent, 
    market_agent_prompt
)

market_finance_agent_executor = AgentExecutor(
    agent=market_finance_agent,
    tools=tools_for_market_agent
)

# Personalized Finance Agent
personalized_agent_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are a versatile and intelligent AI assistant, designed to help the user in a personalized and friendly manner. You excel at answering {messages}, performing calculations, analyzing stock performance, fetching real-time information from various sources like Firestore, and providing localized insights. You always prioritize what benefits the user and can handle complex queries seamlessly. If a request is beyond your scope, you politely decline without revealing internal logic or processes. Don't hallucinate. If you don't know or can't do something, just tell it",
    ),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

personalized_finance_agent = create_tool_calling_agent(model, tools_for_personalized_agent, personalized_agent_prompt)

personalized_finance_agent_executor = AgentExecutor(
    agent=personalized_finance_agent,
    tools=tools_for_personalized_agent
)