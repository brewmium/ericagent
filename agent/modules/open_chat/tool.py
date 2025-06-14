# modules/open_chat/tool.py

from agent.llm_interface import cheap_llm_query

def run(input_data):
    user_input = input_data.get("user_input", "")
    return cheap_llm_query(user_input)
