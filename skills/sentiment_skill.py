import requests
from bs4 import BeautifulSoup
from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

async def get_sentiment(ticker: str) -> str:
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_table = soup.find(id='news-table')
    if not news_table:
        return f"No news found for {ticker}."

    rows = news_table.find_all('tr')[:20]
    headlines = [row.a.get_text() for row in rows if row.a]
    if not headlines:
        return f"No headlines found for {ticker}."

    sentiments = sentiment_pipeline(headlines)

    summary = []
    for hl, sent in zip(headlines, sentiments):
        summary.append(f"- {hl} → {sent['label']} ({sent['score']:.2f})")

    return f"News Sentiment for {ticker} (last 20 headlines):\n" + "\n".join(summary)


