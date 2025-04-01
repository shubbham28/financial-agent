# 🧠 Financial Analysis Agent with LLMs & Semantic Kernel

A modular AI agent that performs real-time financial data analysis, sentiment extraction, and generates smart summaries using:
- 📈 Yahoo Finance data
- 🧠 Semantic Kernel
- 🤗 FinBERT for sentiment
- 🦙 LLaMA for prompt validation
- 🖥️ Streamlit for chatbot UI

---

## 🚀 Features
- ✅ Real-time stock analysis (EMA, RSI, MACD, Bollinger Bands)
- 📰 Live news sentiment from Finviz using FinBERT
- 🧠 LLM-generated summary of trends and predictions
- 🧪 Input validation using Hugging Face's LLaMA API
- 💬 Chatbot-style UI with Streamlit

---

## 🔧 Installation

```bash
git clone https://github.com/shubbham28/financial-agent.git
cd financial-agent
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```
The app launches in your browser with a chat-style interface. Ask things like:
- `TSLA`
- `AAPL for last 7 days at 1hr interval`
- `TSLA, AAPL, Google`

---

## 🔐 Configuration
Update `config/model_config.yaml` with your OpenAI and Hugging Face keys:
```yaml
openai:
  api_key: "your-openai-key"
huggingface:
  api_key: "your-huggingface-key"
  model: "meta-llama/Llama-2-7b-chat-hf"
```

Use `.env` or Hugging Face Secrets for production deployment.

---

## 📁 Project Structure
```
financial_agent/
├── app.py                 # Streamlit interface
├── agent_kernel.py        # SK setup + skill registration
├── config/                # API keys, prompt templates
├── skills/                # Modular skills (finance, sentiment, summary)
├── requirements.txt       # Dependencies
└── README.md              # You are here
```

---

## 📦 Deployment
- GitHub: Push this repo
- Hugging Face: Create a Streamlit Space, upload this project, and set secrets.

---

## ✨ Acknowledgements
- OpenAI GPT for summarization
- ProsusAI FinBERT for sentiment
- Hugging Face for hosting + models
- Microsoft Semantic Kernel for skill orchestration

---

## 🧪 Future Ideas
- Add prediction via regression models
- Integrate news from other sources
- Use LangChain + memory

---

## 📜 License
MIT License
