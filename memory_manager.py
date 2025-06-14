# memory_manager.py

import os
import json
import uuid
from datetime import datetime

MEMORY_DIR = "memory"
ACTIVE_BUCKET_FILE = os.path.join(MEMORY_DIR, "active_bucket.txt")

# Ensure the memory dir exists
os.makedirs(MEMORY_DIR, exist_ok=True)

def _bucket_path(bucket_id):
    return os.path.join(MEMORY_DIR, f"{bucket_id}.json")

def _now():
    return datetime.utcnow().isoformat()

def create_bucket(description=""):
    bucket_id = str(uuid.uuid4())[:8]
    bucket = {
        "bucket_id": bucket_id,
        "task_description": description,
        "created": _now(),
        "last_used": _now(),
        "messages": [],
        "tool_calls": [],
        "tags": []
    }
    with open(_bucket_path(bucket_id), "w") as f:
        json.dump(bucket, f, indent=2)
    set_active_bucket(bucket_id)
    return bucket_id

def load_bucket(bucket_id):
    with open(_bucket_path(bucket_id), "r") as f:
        return json.load(f)

def save_bucket(bucket):
    bucket["last_used"] = _now()
    with open(_bucket_path(bucket["bucket_id"]), "w") as f:
        json.dump(bucket, f, indent=2)

def set_active_bucket(bucket_id):
    with open(ACTIVE_BUCKET_FILE, "w") as f:
        f.write(bucket_id)

def get_active_bucket_id():
    if not os.path.exists(ACTIVE_BUCKET_FILE):
        return create_bucket("Default session")
    with open(ACTIVE_BUCKET_FILE, "r") as f:
        return f.read().strip()

def get_active_bucket():
    return load_bucket(get_active_bucket_id())

def update_memory(role, content):
    bucket = get_active_bucket()
    bucket["messages"].append({"role": role, "content": content})
    save_bucket(bucket)

def record_tool_call(tool_id, args, response):
    bucket = get_active_bucket()
    bucket["tool_calls"].append({
        "dtm": _now(),
        "tool_id": tool_id,
        "args": args,
        "response": response
    })
    save_bucket(bucket)