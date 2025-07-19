AOF_FILENAME = "appendonly.aof"
AOF_ENABLED = True

def disable_aof():
    global AOF_ENABLED
    AOF_ENABLED = False

def enable_aof():
    global AOF_ENABLED
    AOF_ENABLED = True

def append_to_aof(tokens):
    """
    Appends the given token list (command) to the AOF file.
    Example: ['SET', 'key', 'value']
    """
    if not AOF_ENABLED:
        return
    try:
        line = " ".join(tokens) + '\n'
        with open(AOF_FILENAME , "a") as f:
            f.write(line)
    except Exception as e:
        print(f"[AOF] Failed to write: {e}")

def replay_aof():
    """
    Reads the AOF file and returns a list of command token lists.
    Each line is split into tokens like: ['SET', 'key', 'value']
    """
    commands = []
    try:
        with open(AOF_FILENAME, "r") as f:
            for line in f:
                tokens = line.strip().split()
                if tokens:
                    commands.append(tokens)
    except FileNotFoundError:
        pass
    return commands
