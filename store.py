import time

db = {}
expires = {}

def set_key(key, value):
    db[key] = value
    return True

def get_key(key):
    if is_expired(key):
        delete_key(key)
        return None
    return  db.get(key)

def delete_key(key):
    db.pop(key, None)
    expires.pop(key, None)
    return True

def flush_all():
    db.clear()
    expires.clear()
    return True

def is_expired(key):
    return key in expires and time.time() > expires[key]

def set_expiry(key, seconds):
    if key not in db:
        return False
    expires[key] = time.time() + seconds
    return True

def get_ttl(key):
    if key not in db:
        return -2
    if key not in expires:
        return -1
    remaining = expires[key] - time.time()
    return int(remaining) if remaining > 0 else -2
