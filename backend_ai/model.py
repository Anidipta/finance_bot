import json
from typing import Optional, Dict, Any, List
from model_config import (
    model,
    market_finance_agent_executor,
    personalized_finance_agent_executor,
    classification_chain
)
from langchain_core.messages import HumanMessage, AIMessage
from tools import *

async def process_chat(message: str, id: str) -> List[str]:
    """
    Process an incoming chat message and return a list containing:
      [classified intent, response]
    Allowed intents: greeting, personalized, real time, or general.
    """
    chat_history = []  
    formatted_history = [
        HumanMessage(content=chat["message"]) if i % 2 == 0 
        else AIMessage(content=chat["response"])
        for i, chat in enumerate(chat_history)
    ]

    intent = classification_chain.invoke({
        "chat_history": formatted_history,
        "query": message
    })

    response = None
    intent_lower = intent.lower()
    if "greeting" in intent_lower or "who are you" in intent_lower:
        response = "Hello, my name is FinGPT, made by Team FinGPT."
    elif "personalized" in intent_lower:
        response = await handle_personalized_query(message, id)
    elif "real time" in intent_lower or "market" in intent_lower:
        response = await handle_market_query(message)
    elif "general" in intent_lower:
        response = await handle_general_query(message)
    else:
        response = ("I'm sorry, I can only answer queries about general market and finance info, "
                    "personalized stock data, greetings, or real-time market data.")
    
    return [intent, response]

async def handle_market_query(message: str) -> str:
    """
    Handle market data related queries using the market agent executor.
    """
    try:
        result = market_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=message)]
        })
        return result.get("output", "Sorry, I couldn't process that request.")
    except Exception as e:
        return f"Error processing market query: {str(e)}"

async def handle_personalized_query(message: str, user_id: str) -> str:
    """
    Handle personalized queries by dynamically injecting user's real portfolio context.
    """
    try:
        portfolio_data = get_user_portfolio(user_id)
        
        if "error" in portfolio_data:
            return f"Could not retrieve portfolio: {portfolio_data['error']}"

        contextualized_message = (
            f"User portfolio: {portfolio_data}\n\n"
            f"Query: {message}"
        )

        result = personalized_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=contextualized_message)]
        })

        return result.get("output", "Sorry, I couldn't process that request.")
    
    except Exception as e:
        return f"Error processing personalized query: {str(e)}"

async def handle_general_query(message: str) -> str:
    """
    Handle general queries using the base model.
    """
    try:
        response = model.invoke([HumanMessage(content=message)])
        return response.content
    except Exception as e:
        return f"Error processing general query: {str(e)}"
