
# memory.py
# Simple in-memory storage (safe for STEP 2)

user_memory = {}

def set_name(user_id, name):
    user_memory[user_id] = name

def get_name(user_id):
    return user_memory.get(user_id)
