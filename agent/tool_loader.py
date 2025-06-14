# tool_loader.py

import os
import json
import importlib.util
from pathlib import Path

MODULES_PATH = Path(__file__).parent / "modules"  # ← fixed here

class Tool:
    def __init__(self, tool_id, manifest, module):
        self.tool_id = tool_id
        self.manifest = manifest
        self.module = module
        self.entry_point = getattr(module, "run", None)

    def execute(self, input_data):
        if not self.entry_point:
            raise RuntimeError(f"No entry point in tool {self.tool_id}")
        return self.entry_point(input_data)

def load_tools():
    tool_registry = {}

    for tool_path in MODULES_PATH.iterdir():
        if not tool_path.is_dir():
            continue

        cart_path = tool_path / "cart.json"
        code_path = tool_path / "tool.py"

        if not cart_path.exists() or not code_path.exists():
            continue

        with cart_path.open("r") as f:
            manifest = json.load(f)

        spec = importlib.util.spec_from_file_location(
            f"{tool_path.name}_module", code_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        tool = Tool(tool_path.name, manifest, module)
        tool_registry[tool_path.name] = tool

    return tool_registry