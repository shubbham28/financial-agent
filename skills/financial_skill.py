import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

async def analyze_stock(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    df = yf.Ticker(ticker).history(period=period, interval=interval)
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['Volatility'] = df['Close'].rolling(window=5).std()
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['Signal'] = df['MACD'].ewm(span=9).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['Upper_BB'] = df['MA_5'] + (2 * df['Volatility'])
    df['Lower_BB'] = df['MA_5'] - (2 * df['Volatility'])

    latest = df.iloc[-1]
    ma = latest['MA_5']
    vol = latest['Volatility']
    trend = "Uptrend" if latest['Close'] > ma else "Downtrend"

    # Save plot
    plt.figure(figsize=(10, 4))
    df['Close'].plot(label='Close')
    df['MA_5'].plot(label='MA_5')
    df['EMA_10'].plot(label='EMA_10')
    plt.title(f"{ticker.upper()} Price, MA, and EMA")
    plt.legend()
    path = f"outputs/{ticker.upper()}_plot.png"
    os.makedirs("outputs", exist_ok=True)
    plt.savefig(path)
    plt.close()

    return f"{ticker.upper()} Analysis:\nPrice: {latest['Close']:.2f}\nMA(5): {ma:.2f}\nEMA(10): {latest['EMA_10']:.2f}\nVolatility: {vol:.4f}\nRSI: {latest['RSI']:.2f}\nMACD: {latest['MACD']:.2f}\nSignal: {latest['Signal']:.2f}\nTrend: {trend}\nPlot saved at {path}"
