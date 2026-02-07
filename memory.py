import time

MEMORY = {}
TTL = 10 * 24 * 60 * 60  # 10 days

def save_message(user_id, role, content):
    now = time.time()
    MEMORY.setdefault(user_id, [])
    MEMORY[user_id].append({
        "role": role,
        "content": content,
        "time": now
    })
    MEMORY[user_id] = [
        m for m in MEMORY[user_id] if now - m["time"] < TTL
    ]

def get_memory(user_id):
    if user_id not in MEMORY:
        return []
    return [{"role": m["role"], "content": m["content"]} for m in MEMORY[user_id]]
