from store import (
    set_key, get_key, delete_key,
    flush_all, set_expiry, get_ttl
)
from aof import append_to_aof

def execute_command(tokens):
    if not tokens:
        return None

    cmd = tokens[0].upper()

    if cmd == "SET":
        return handle_set(tokens)
    elif cmd == "GET":
        return handle_get(tokens)
    elif cmd == "DEL":
        return handle_del(tokens)
    elif cmd == "FLUSH":
        return handle_flush(tokens)
    elif cmd == "EXPIRE":
        return handle_expire(tokens)
    elif cmd == "TTL":
        return handle_ttl(tokens)
    elif cmd == "MSET":
        return handle_mset(tokens)
    elif cmd == "MGET":
        return handle_mget(tokens)
    else:
        return "-ERROR unknown command"

def handle_set(tokens):
    if len(tokens) != 3:
        return "-ERROR SET requires 2 arguments"
    append_to_aof(tokens)
    key,value = tokens[1], tokens[2]
    return set_key(key, value)

def handle_get(tokens):
    if len(tokens) != 2:
        return "-ERROR GET requires 1 argument"
    return get_key(tokens[1])

def handle_del(tokens):
    if len(tokens) != 2:
        return "-ERROR DEL requires 1 argument"
    append_to_aof(tokens)
    return delete_key(tokens[1])

def handle_flush(tokens):
    return flush_all()

def handle_ttl(tokens):
    if len(tokens) != 2:
        return "-ERROR TTL requires 1 argument"
    return get_ttl(tokens[1])

def handle_expire(tokens):
    if len(tokens) != 3:
        return "-ERROR EXPIRE requires 2 arguments"
    try:
        seconds = int(tokens[2])
        success = set_expiry(tokens[1], seconds)
        return success or None
    except ValueError:
        return "-ERROR invalid TTL"

def handle_mset(tokens):
    if (len(tokens) - 1) % 2 != 0:
        return "-ERROR MSET requires an even number of arguments"

    append_to_aof(tokens)
    for i in range(1,len(tokens),2):
        key = tokens[i]
        value = tokens[i+1]
        set_key(key, value)

    return True

def handle_mget(tokens):
    if len(tokens) < 2:
        return "-ERROR MGET requires at least 2 arguments"

    values = []
    for key in tokens[1:]:
        value = get_key(key)
        values.append(value)

    return values
