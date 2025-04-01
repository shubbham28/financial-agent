import streamlit as st
import asyncio
import requests
import yaml
from skills import financial_skill, sentiment_skill, summary_skill
import openai
import re
import yfinance as yf
import datetime

st.set_page_config(page_title="Financial Chatbot", layout="wide")
st.title("💬 Financial Analysis Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

# kernel = create_kernel()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

with open("config/model_config.yaml", "r") as f:
    config = yaml.safe_load(f)

def classify_prompt(prompt):
    """
    Classifies the given user prompt as 'valid' or 'invalid' based on:
    - Presence of known stock tickers or names in config/stock_info.csv
    - Fallback to OpenAI GPT model for format-based validation

    Parameters:
    - prompt (str): The user input to classify.

    Returns:
    - str: 'valid' if the prompt adheres to specified formats or matches stock list, otherwise 'invalid'.
    """
    # Extract words from prompt
    words = re.findall(r'\b\w{4,}\b', prompt.lower())  # Words longer than 3 characters

    for word in words:
        try:
            df = yf.Ticker(word).history(period="1d")
            if not df.empty:
                return 'valid'
        except Exception:
            continue  # If yfinance fails silently, skip the word


    # Define the instruction for the model
    with open("config/model_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    openai.api_key = config["openai"]["api_key"]
    instruction = (
        "Please classify the following user prompt as 'valid' or 'invalid'. "
        "A valid prompt relates to stock tickers in the formats: "
        "(1) a single ticker symbol (e.g., 'TSLA'), "
#         "(2) a ticker symbol followed by a time frame (e.g., 'AAPL for last 5 days at 1hr interval'), or "
        "(2) multiple ticker symbols separated by commas (e.g., 'TSLA, AAPL, Google'). "
        "Respond with only 'valid' or 'invalid'."
    )

    # Combine the instruction with the user prompt
    full_prompt = f"{instruction}\n\nUser Prompt: '{prompt}'"

    try:
        # Send the prompt to the OpenAI API
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",  # Use the appropriate engine
            prompt=full_prompt,
            max_tokens=10  # Limit the response length
        )
        # Extract and return the classification result
        result = response.choices[0].text.strip().lower()
        if result in ['valid', 'invalid']:
            return result
        else:
            return 'invalid'  # Default to 'invalid' for unexpected responses
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'invalid'

def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M")

user_input = st.chat_input("Ask about a stock (e.g., TSLA or AAPL) or a list of stocks (e.g., TSLA, AAPL, GOOG)")

if user_input:
    timestamp = get_timestamp()

    # Store user input (but don't render it here)
    st.session_state.history.append({
        "role": "user",
        "type": "text",
        "content": user_input,
        "time": timestamp
    })

    # Process after input is added to history
    with st.spinner("Validating and analyzing stock(s)..."):
        if classify_prompt(user_input) != "valid":
            st.session_state.history.append({
                "role": "agent",
                "type": "text",
                "content": "❌ Invalid input. Please use formats like: 'TSLA', 'Tesla', 'AAPL for last 5 days at 1hr interval', or a list like 'TSLA, AAPL'.",
                "time": get_timestamp()
            })
        else:
            tickers = re.split(r'[,\s]+', user_input.strip())
            tickers = [token for token in tickers if token]
            for ticker in tickers:
                try:
                    df = yf.Ticker(ticker).history(period="1d")
                    if not df.empty:
                        analysis = loop.run_until_complete(financial_skill.analyze_stock(ticker))
                        sentiment = loop.run_until_complete(sentiment_skill.get_sentiment(ticker))
                        text_input = f"\n{analysis}\n\nList of articles and followed by their sentiment and confidence\n\n{sentiment}\n"
                        summary = loop.run_until_complete(summary_skill.summarize(text_input))

                        now = get_timestamp()
                        st.session_state.history.append({
                            "role": "agent",
                            "type": "combo",
                            "summary": f"🧠 **{ticker} Analysis Summary**\n\n{summary}",
                            "analysis": f"📊 **Analysis**\n\n{analysis}",
                            "sentiment": f"📰 **Sentiment**\n\n{sentiment}",
                            "image": f"outputs/{ticker}_plot.png",
                            "time": now
                        })
                except Exception:
                    continue

# 🔁 Replay full conversation from state (including latest input)
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        timestamp = msg.get("time", "")
        header = f"{timestamp}"
        st.markdown(f"**{header}**")

        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "combo":
            st.markdown(msg["summary"])
            st.markdown(msg["analysis"])
            st.markdown(msg["sentiment"])
            st.image(msg["image"])

