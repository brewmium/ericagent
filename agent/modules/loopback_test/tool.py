# modules/loopback_test/tool.py

def run(input_data):
    user_input = input_data.get("user_input", "")
    return {
        "response": f"{user_input}",
        "source": "loopback_test"
    }