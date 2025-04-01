import yaml
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
from semantic_kernel.prompt_template.prompt_template_engine import PromptTemplateEngine

async def summarize(text: str) -> str:
    with open("config/prompt_templates.yaml", "r") as f:
        templates = yaml.safe_load(f)
    prompt = templates["summary_prompt"]
    context = ContextVariables()
    context["input"] = text
    return PromptTemplateEngine().render(prompt, context)
