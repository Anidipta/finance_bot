from ..config import model, market_finance_agent_executor, personalized_finance_agent_executor, classification_chain
from ..database import FirestoreDB
from langchain_core.messages import HumanMessage, AIMessage
from typing import Optional, Dict, Any, List

async def process_chat(message: str, user_id: str, email: Optional[str] = None) -> str:
    """Process chat messages and return AI response"""
    # Get chat history
    chat_history = await FirestoreDB.get_chat_history(user_id)
    
    # Convert chat history to LangChain message format
    formatted_history = [
        HumanMessage(content=chat["message"]) if i % 2 == 0 
        else AIMessage(content=chat["response"])
        for i, chat in enumerate(chat_history)
    ]

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

    # Store chat in database
    await FirestoreDB.store_chat(user_id, email, message, response)
    
    return response

async def handle_market_query(message: str) -> str:
    """Handle market data related queries"""
    try:
        result = market_finance_agent_executor.invoke({
            "messages": [HumanMessage(content=message)]
        })
        return result.get("output", "Sorry, I couldn't process that request.")
    except Exception as e:
        return f"Error processing market query: {str(e)}"

async def handle_personalized_query(message: str, user_id: str) -> str:
    """Handle personalized advice queries"""
    try:
        # Get user portfolio for context
        portfolio = await FirestoreDB.get_user_portfolio(user_id)
        
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
    """Analyze a stock position"""
    from ..tools import calculate_profit_loss, stock_performance_analysis
    
    current_data = await handle_market_query(f"Get current price for {ticker}")
    current_price = current_data.get("regularMarketPrice", 0)
    
    analysis = {
        "profit_loss": calculate_profit_loss(ticker, purchase_price, quantity, current_price),
        "performance": stock_performance_analysis(ticker),
        "current_price": current_price
    }
    
    return analysis 