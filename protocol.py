def parse_request(data: bytes) -> list:
    try:
        text = data.decode().strip()
        if not text:
            return []
        return text.split()
    except UnicodeDecodeError:
        return []

def encode_response(result) -> bytes:
    if result is None:
        return b"$-1\r\n"
    elif isinstance(result,str):
        return f"${len(result)}\r\n{result}\r\n".encode()
    elif isinstance(result, list):
        resp = f"*{len(result)}\r\n"
        for item in result:
            if item is None:
                resp += "$-1\r\n"
            else:
                resp += f"${len(str(item))}\r\n{item}\r\n"
        return resp.encode()
    elif result is True:
        return b"+OK\r\n"
    elif result is False:
        return b"-ERROR\r\n"
    else:
        return f"{result}\r\n".encode()
        
# if __name__ == "__main__":
#     print(parse_request(b"SET foo bar\r\n"))
#     print(encode_response("hello"))
#     print(encode_response(None))
#     print(encode_response(["one", None, "three"]))
