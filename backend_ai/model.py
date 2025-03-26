import os
import sys
from typing import Optional, Dict, Any, List

from model_config import initialize_models
initialize_models()

from model_config import model, market_finance_agent_executor, personalized_finance_agent_executor, classification_chain
from langchain_core.messages import HumanMessage, AIMessage

from tools import *

async def process_chat(message: str, user_id: str = '123', email: Optional[str] = None) -> List[str]:
    """Process chat messages and return AI response for four allowed intents."""
    chat_history = []  # In a real scenario, you'd populate this with previous conversation turns
    
    formatted_history = [
        HumanMessage(content=chat["message"]) if i % 2 == 0 
        else AIMessage(content=chat["response"])
        for i, chat in enumerate(chat_history)
    ]

    # Use the classification chain to get a simplified intent label.
    intent = classification_chain.invoke({
        "chat_history": formatted_history,
        "query": message
    })

    response = None
    intent_lower = intent.lower()
    if "greeting" in intent_lower or "who are you" in intent_lower:
        response = "Hello, my name is FinGPT, made by Team FinGPT."
    elif "personalized" in intent_lower:
        response = await handle_personalized_query(message, user_id)
    elif "real time" in intent_lower or "market" in intent_lower:
        response = await handle_market_query(message)
    elif "general" in intent_lower:
        response = await handle_general_query(message)
    else:
        response = ("I'm sorry, I can only answer queries about general market and finance info, "
                    "personalized stock data, greetings, or real-time market data.")
    
    return [intent, response]

async def handle_market_query(message: str) -> str:
    """Handle market data related queries"""
    try:
        result = market_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=message)]
        })
        return result.get("output", "Sorry, I couldn't process that request.")
    except Exception as e:
        return f"Error processing market query: {str(e)}"

async def handle_personalized_query(message: str, user_id: str = '123') -> str:
    """Handle personalized advice queries"""
    try:
        # Example: add a dummy portfolio context for personalized queries
        portfolio = {"stocks": ["AAPL", "GOOGL"], "cash": 10000}
        contextualized_message = f"User portfolio: {portfolio}\n\nQuery: {message}"
        
        result = personalized_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=contextualized_message)]
        })
        return result.get("output", "Sorry, I couldn't process that request.")
    except Exception as e:
        return f"Error processing personalized query: {str(e)}"

async def handle_general_query(message: str) -> str:
    """Handle general information queries"""
    try:
        response = model.invoke([HumanMessage(content=message)])
        return response.content
    except Exception as e:
        return f"Error processing general query: {str(e)}"

async def analyze_stock_position(ticker: str, quantity: int, purchase_price: float) -> Dict[str, Any]:
    """Analyze a stock position"""
    from tools import calculate_profit_loss, stock_performance_analysis
    
    current_data = await handle_market_query(f"Get current price for {ticker}")
    current_price = current_data.get("regularMarketPrice", 0)
    
    analysis = {
        "profit_loss": calculate_profit_loss(ticker, purchase_price, quantity, current_price),
        "performance": stock_performance_analysis(ticker),
        "current_price": current_price
    }
    
    return analysis
