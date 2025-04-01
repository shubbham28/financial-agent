from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion
from skills import financial_skill, sentiment_skill, summary_skill
import yaml

def create_kernel():
    with open("config/model_config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    kernel = Kernel()
    kernel.add_text_completion_service("openai-gpt", OpenAITextCompletion(
        service_id="openai-gpt",
        api_key=cfg["openai"]["api_key"],
        model=cfg["openai"]["model"]
    ))

    kernel.import_skill({
        "AnalyzeStock": financial_skill.analyze_stock,
        "GetSentiment": sentiment_skill.get_sentiment,
        "Summarize": summary_skill.summarize
    }, skill_name="Finance")

    return kernel