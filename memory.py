# memory.py
# Basanti Bot Memory System

from collections import defaultdict, deque

# har user ki short-term memory
user_memory = defaultdict(lambda: deque(maxlen=10))

# user preferences (language, name etc.)
user_profile = defaultdict(dict)


def save_message(user_id, role, text):
    """
    role: 'user' ya 'bot'
    text: message content
    """
    user_memory[user_id].append({
        "role": role,
        "text": text
    })


def get_context(user_id):
    """
    last few messages ka context return karega
    """
    return list(user_memory[user_id])


def set_preference(user_id, key, value):
    user_profile[user_id][key] = value


def get_preference(user_id, key, default=None):
    return user_profile[user_id].get(key, default)


def clear_memory(user_id):
    user_memory[user_id].clear()
