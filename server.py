from gevent import monkey
monkey.patch_all()

import socket
from protocol import parse_request, encode_response
from commands import execute_command
from aof import replay_aof, disable_aof, enable_aof
import gevent
from gevent.server import StreamServer

def handle_client(socket, address):
    print(f"[CONNECT] New connection from {address}")
    try:
        while True:
            # Receive data from client (up to 1024 bytes)
            data = socket.recv(1024)
            if not data:
                break      # client disconnected
                
            tokens = parse_request(data)
            result = execute_command(tokens)
            response = encode_response(result)
            # Echo the data back to the client a Redis-like response
            socket.sendall(response)
    except Exception as e:
        print(f"[ERROR] Client {address}: {e}")
    finally:
        socket.close()
        print(f"[DISCONNECT] {address} disconnected")

def start_gevent_server(host="127.0.0.1",port=6379):
    preload_from_aof()
    server = StreamServer((host, port), handle_client)
    print(f"[SERVER] Listening on {host}:{port}")
    server.serve_forever()

def preload_from_aof():
    """Replays AOF commands at startup to restore state."""
    print("[BOOT] Replaying AOF file")
    disable_aof()
    commands = replay_aof()
    count = 0
    for cmd in commands:
        execute_command(cmd)
        count += 1
    enable_aof()
    print(f"[BOOT] Loaded {count} command(s) from AOF")

if __name__ == '__main__':
    start_gevent_server()
