from tool_loader import load_tools
from llm_interface.local_llm import llm_query, LocalLLMUnavailable
from llm_interface import local_llm_query, cheap_llm_query, expensive_llm_query, COST_CHEAP, COST_EXPENSIVE
from memory_manager import update_memory, record_tool_call

print("✅ Supervisor.py loaded and running")

def supervisor(prompt: str) -> str:
    try:
        return llm_query(prompt)
    except LocalLLMUnavailable as e:
        print(f"[Supervisor Notice] {e} — Falling back to cheap remote model.")
        return cheap_llm_query(prompt)
    

TOOLS = load_tools()
MAX_BUDGET_DOLLARS = 0.005  # set your per-call cap

def decide_tool(user_input: str) -> str:
    prompt = f"""
You are a Supervisor agent. Your job is to pick the best tool to handle a request.
Available tools: {', '.join(TOOLS.keys())}
User input: "{user_input}"
Return only the name of the best tool, no explanation.
"""

    print("🔍 [Supervisor] Trying local LLM...")
    local_response = local_llm_query(prompt).strip().lower()
    if local_response in TOOLS:
        print(f"✅ [Local LLM] chose: {local_response}")
        return local_response

    print("💸 [Supervisor] Trying cheap remote LLM...")
    cheap_response = cheap_llm_query(prompt).strip().lower()
    if cheap_response in TOOLS:
        print(f"✅ [Cheap LLM] chose: {cheap_response}")
        return cheap_response

    print("🧠 [Supervisor] Trying expensive LLM...")
    rich_response = expensive_llm_query(prompt).strip().lower()
    if rich_response in TOOLS:
        print(f"✅ [Expensive LLM] chose: {rich_response}")
        return rich_response

    print("🚨 No valid response — falling back to loopback_test")
    return "loopback_test"

if __name__ == "__main__":
    print("🤖 EricsAgent online. Type something!")
    while True:
        user_input = input("👤 You: ")
        if user_input.strip().lower() in ["quit", "exit"]:
            break
        chosen_tool = decide_tool(user_input)
        print(f"🧭 [Supervisor] Chose tool: {chosen_tool}")
        result = TOOLS[chosen_tool].execute({"user_input": user_input})
        source = result.get("source", chosen_tool)
        tokens = result.get("tokens", "?")
        cost = result.get("cost", "?")
        print(f"🤖 Agent [{source}, {tokens} tokens, ${cost} est. cost]: {result['response']}")
