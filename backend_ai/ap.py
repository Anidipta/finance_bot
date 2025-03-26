import streamlit as st
import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api"

def create_user(email: str, username: str):
    """Create a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/users", 
            json={
                "email": email, 
                "username": username
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error creating user: {e}")
        return None

def send_chat_message(message: str, user_id: str = None, email: str = None):
    """Send chat message to backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat", 
            json={
                "message": message, 
                "user_id": user_id,
                "email": email
            }
        )
        response.raise_for_status()
        return response.json().get("response", "No response")
    except requests.RequestException as e:
        st.error(f"Error sending message: {e}")
        return "Sorry, there was an error processing your request."

def analyze_stock(ticker: str, quantity: int, purchase_price: float):
    """Analyze stock position"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/stock-analysis", 
            json={
                "ticker": ticker, 
                "quantity": quantity, 
                "purchase_price": purchase_price
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error analyzing stock: {e}")
        return None

def main():
    st.title("Financial AI Assistant")

    # User Authentication Section
    st.sidebar.header("User Authentication")
    with st.sidebar.form("user_form"):
        email = st.text_input("Email")
        username = st.text_input("Username")
        submit_user = st.form_submit_button("Create/Login User")
        
        if submit_user:
            user = create_user(email, username)
            if user:
                st.sidebar.success("User authenticated!")
                st.session_state['user_id'] = user.get('user_id')
                st.session_state['email'] = email

    # Chat Interface
    st.header("Chat with Financial AI")
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display chat history
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a financial question"):
        # Add user message to chat history
        st.session_state['messages'].append({
            "role": "user", 
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_chat_message(
                    prompt, 
                    user_id=st.session_state.get('user_id'),
                    email=st.session_state.get('email')
                )
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state['messages'].append({
            "role": "assistant", 
            "content": response
        })

    # Stock Analysis Section
    st.header("Stock Position Analysis")
    with st.form("stock_analysis"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.text_input("Stock Ticker")
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        with col3:
            purchase_price = st.number_input("Purchase Price", min_value=0.01, format="%.2f")
        
        analyze_button = st.form_submit_button("Analyze Stock")
        
        if analyze_button:
            with st.spinner("Analyzing stock..."):
                analysis = analyze_stock(ticker, quantity, purchase_price)
                if analysis:
                    st.json(analysis)

if __name__ == "__main__":
    main()