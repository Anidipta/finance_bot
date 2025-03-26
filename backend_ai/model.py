import os
import sys
from typing import Optional, Dict, Any, List

from model_config import model, market_finance_agent_executor, personalized_finance_agent_executor, classification_chain
from langchain_core.messages import HumanMessage, AIMessage

# Import all tools from the tools file
from tools import (
    company_information,
    calculate_profit_loss,
    stock_performance_analysis
)

async def process_chat(message: str, user_id: str='123', email: Optional[str] = None) -> str:
    """Process chat messages and return AI response"""
    # Dummy chat history for testing
    chat_history = []
    
    # Convert chat history to LangChain message format
    formatted_history = []

    # Classify intent
    intent = classification_chain.invoke({
        "chat_history": formatted_history,
        "query": message
    })

    # Process based on intent
    response = None
    if "Market" in intent:
        response = await handle_market_query(message)
    elif "Personalized" in intent:
        response = await handle_personalized_query(message, user_id)
    else:
        response = await handle_general_query(message)
    
    return [intent,response]

async def handle_market_query(message: str) -> str:
    """Handle market data related queries"""
    try:
        result = market_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=message)]
        })
        return result.get("output", "Sorry, I couldn't process that request.")
    except Exception as e:
        return f"Error processing market query: {str(e)}"

async def handle_personalized_query(message: str, user_id: str='123') -> str:
    """Handle personalized advice queries"""
    try:
        # Add a mock portfolio for testing
        portfolio = {"stocks": ["AAPL", "GOOGL"], "cash": 10000}
        
        # Add portfolio context to message
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
    """Analyze a stock position using tools"""
    try:
        # Get company information to fetch current price
        company_info = company_information(ticker)
        current_price = company_info.get('regularMarketPrice', purchase_price)
        
        # Calculate profit/loss
        profit_loss_analysis = calculate_profit_loss(
            ticker, 
            purchase_price, 
            quantity, 
            current_price
        )
        
        # Get stock performance
        performance_analysis = stock_performance_analysis(ticker)
        
        # Combine analyses
        analysis = {
            "profit_loss": profit_loss_analysis,
            "performance": performance_analysis,
            "current_price": current_price,
            "company_info": {
                "name": company_info.get('longName'),
                "sector": company_info.get('sector'),
                "industry": company_info.get('industry')
            }
        }
        
        return analysis
    except Exception as e:
        return {
            "error": f"Error analyzing stock position: {str(e)}",
            "ticker": ticker
        }