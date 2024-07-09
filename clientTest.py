import asyncio
from websockets.sync.client import connect
from time import sleep
import json

with connect("ws://localhost:8765") as websocket:
    # Send data to the server
    for i in range(4):
        websocket.send(json.dumps({'cmd': "drive",
                                "args": {
                                    "vx": 0.0,
                                    "vy": 0.0,
                                    "wz": 0.0
                                    }
                                }).encode())
        sleep(1)

    websocket.send(json.dumps({'cmd': "drive",
                                "args": {
                                    "vx": 0.0,
                                    "vy": 0.0,
                                    "wz": 0.0
                                    }
                                }).encode())
    sleep(1)

    for i in range(5):
        websocket.send(json.dumps({'cmd': "read_lidar"}).encode())
        sleep(1)
        data = websocket.recv()
        json_data = json.loads(data.decode())
        print(json_data)