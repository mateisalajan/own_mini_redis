AOF_FILENAME = "appendonly.aof"

def append_to_aof(tokens):
    """
    Appends the given token list (command) to the AOF file.
    Example: ['SET', 'key', 'value']
    """
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
