import requests
from bs4 import BeautifulSoup
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np

# Load FinBERT tokenizer and model manually
model_name = "ProsusAI/finbert"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
model.eval()

# Label order used by FinBERT
labels = ['negative', 'neutral', 'positive']

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

    summary = []
    for hl in headlines:
        inputs = tokenizer(hl, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1).numpy()[0]
            label_index = np.argmax(probs)
            label = labels[label_index]
            score = probs[label_index]
        summary.append(f"- {hl} → {label.title()} ({score:.2f})")

    return f"News Sentiment for {ticker} (last 20 headlines):\n" + "\n".join(summary)
