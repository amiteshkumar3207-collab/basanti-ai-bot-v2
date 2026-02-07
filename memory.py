import time

# In-memory storage (later DB/vector me shift ho sakta hai)
SHORT_MEMORY = {}
LONG_MEMORY = {}

SHORT_TTL = 60 * 60          # 1 hour
LONG_TTL = 21 * 24 * 60 * 60 # 21 days

def _cleanup(store, ttl):
    now = time.time()
    for uid in list(store.keys()):
        store[uid] = [m for m in store[uid] if now - m["time"] < ttl]
        if not store[uid]:
            del store[uid]

def save_short(user_id, role, content):
    now = time.time()
    SHORT_MEMORY.setdefault(user_id, [])
    SHORT_MEMORY[user_id].append({
        "role": role,
        "content": content,
        "time": now
    })
    _cleanup(SHORT_MEMORY, SHORT_TTL)

def save_long(user_id, key, value):
    now = time.time()
    LONG_MEMORY.setdefault(user_id, {})
    LONG_MEMORY[user_id][key] = {
        "value": value,
        "time": now
    }
    _cleanup_long()

def _cleanup_long():
    now = time.time()
    for uid in list(LONG_MEMORY.keys()):
        for k in list(LONG_MEMORY[uid].keys()):
            if now - LONG_MEMORY[uid][k]["time"] > LONG_TTL:
                del LONG_MEMORY[uid][k]
        if not LONG_MEMORY[uid]:
            del LONG_MEMORY[uid]

def get_short(user_id):
    _cleanup(SHORT_MEMORY, SHORT_TTL)
    return [{"role": m["role"], "content": m["content"]} for m in SHORT_MEMORY.get(user_id, [])]

def get_long(user_id):
    _cleanup_long()
    if user_id not in LONG_MEMORY:
        return []
    facts = []
    for k, v in LONG_MEMORY[user_id].items():
        facts.append(f"{k}: {v['value']}")
    return facts
