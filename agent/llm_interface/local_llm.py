# llm_interface/local_llm.py

import subprocess

class LocalLLMUnavailable(Exception):
    pass

def is_ollama_running() -> bool:
    try:
        subprocess.run(
            ["ollama", "list"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def llm_query(prompt: str, model: str = "llama3") -> str:
    if not is_ollama_running():
        raise LocalLLMUnavailable("Local LLM server (Ollama) is not available.")

    try:
        process = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return process.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        raise LocalLLMUnavailable(
            f"Local LLM failed to respond: {e.stderr.decode('utf-8')}"
        )
    