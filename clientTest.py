import socket
from time import sleep
import json

# Create a socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect(('localhost', 1234))

# Send data to the server
for i in range(5):
    client.send(json.dumps({'cmd': "drive",
                            "args": {
                                "vx": 1.0,
                                "vy": 0.0,
                                "wz": 0.0
                                }
                            }).encode())
    sleep(1)

for i in range(5):
    client.send(json.dumps({'cmd': "read_lidar"}).encode())
    sleep(1)
    data = client.recv(1024)
    json_data = json.loads(data.decode())
    print(json_data)


# Close the connection
client.close()