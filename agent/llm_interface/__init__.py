import os
from .local_llm import llm_query as local_llm_query
from .openai_llm import llm_query as remote_llm_query

CHEAP_MODEL = os.getenv("OPENAI_MODEL_CHEAP", "gpt-3.5-turbo")
EXPENSIVE_MODEL = os.getenv("OPENAI_MODEL_EXPENSIVE", "gpt-4o")

COST_CHEAP = float(os.getenv("MODEL_COST_CHEAP", "0.0015"))
COST_EXPENSIVE = float(os.getenv("MODEL_COST_EXPENSIVE", "0.01"))

def cheap_llm_query(prompt: str) -> str:
    return remote_llm_query(prompt, model=CHEAP_MODEL)

def expensive_llm_query(prompt: str) -> str:
    return remote_llm_query(prompt, model=EXPENSIVE_MODEL)
