import streamlit as st
import asyncio
import re
from agent_kernel import create_kernel

st.set_page_config(page_title="Financial Chatbot", layout="wide")
st.title("💬 Financial Analysis Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

kernel = create_kernel()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def is_valid_prompt(prompt):
    ticker_pattern = re.compile(r'^[A-Za-z\s,.-]+$')
    return bool(ticker_pattern.match(prompt))

user_input = st.chat_input("Ask about a stock (e.g., TSLA or AAPL for last 5 days at 1hr interval)")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    if not is_valid_prompt(user_input):
        response = "❌ Invalid input. Please use formats like: 'TSLA', 'Tesla', 'AAPL for last 5 days at 1hr interval', or a list like 'TSLA, AAPL'."
    else:
        tickers = [s.strip().upper() for s in user_input.split(",") if s.strip()]
        response = ""
        for ticker in tickers:
            analysis = loop.run_until_complete(kernel.skills["Finance"]["AnalyzeStock"](ticker))
            sentiment = loop.run_until_complete(kernel.skills["Finance"]["GetSentiment"](ticker))
            summary = loop.run_until_complete(kernel.skills["Finance"]["Summarize"](analysis + "\n" + sentiment))

            response += f"\n\n📊 **{ticker} Analysis**\n{analysis}\n"
            response += f"📰 **Sentiment**\n{sentiment}\n"
            response += f"🧠 **Summary**\n{summary}\n"
            st.image(f"outputs/{ticker}_plot.png")

    st.session_state.history.append({"role": "agent", "content": response})

# Display conversation
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])