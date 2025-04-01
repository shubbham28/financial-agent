import yaml
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelFunction, KernelFunctionFromPrompt
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig

async def summarize(text: str) -> str:
    # Load prompt template
    with open("config/prompt_templates.yaml", "r") as f:
        templates = yaml.safe_load(f)
    prompt_template = templates["summary_prompt"]
    prompt_template = prompt_template.strip()
    
    if not prompt_template:
        raise ValueError("The prompt template is empty after trimming.")
    # Render final prompt
#     rendered_prompt = prompt_template.replace("{{input}}", text)
#     print(rendered_prompt)
    # Create temporary kernel to access OpenAI service
    kernel = Kernel()
    # Load the same config used in agent_kernel.py
    with open("config/model_config.yaml", "r") as f:
        model_config = yaml.safe_load(f)

    kernel.add_service(
        OpenAIChatCompletion(
            service_id="openai-gpt",
            api_key=model_config["openai"]["api_key"],
            ai_model_id=model_config["openai"]["model"]
        )
    )
    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id="openai-gpt",
        ai_model_id=model_config["openai"]["model"],
        temperature=0.7,
    )

    # Define the prompt function
    prompt_template_config = PromptTemplateConfig(
        template=prompt_template,
        name="summarize",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(name="input", description="The user input", is_required=True),
        ],
        execution_settings=execution_settings,
    )

    summarize = kernel.add_function(
        function_name="summarizeFunc",
        plugin_name="summarizePlugin",
        prompt_template_config=prompt_template_config,
    )

    # Invoke the function asynchronously
    result = await kernel.invoke(summarize, input=text)

    return result
