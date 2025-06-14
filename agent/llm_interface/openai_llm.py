# llm_interface/openai_llm.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
default_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

MODEL_COSTS = {
    "gpt-3.5-turbo": 0.0015,  # per 1k tokens
    "gpt-4o": 0.01,
    "gpt-4": 0.03  # in case you use legacy later
}

def llm_query(prompt: str, model: str = default_model) -> dict:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )

        content = response.choices[0].message.content.strip()
        token_count = response.usage.total_tokens
        cost_per_1k = MODEL_COSTS.get(model, 0.01)
        estimated_cost = (token_count / 1000) * cost_per_1k

        return {
            "response": content,
            "source": model,
            "tokens": token_count,
            "cost": f"${estimated_cost:.5f}"
        }

    except Exception as e:
        return {
            "response": f"[Error from OpenAI API: {e}]",
            "source": model,
            "tokens": 0,
            "cost": 0
        }