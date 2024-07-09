import asyncio
from websockets.sync.server import serve
from websockets.exceptions import ConnectionClosedError
from threading import Thread, Lock
import json
from mbot_bridge.api import MBot

mbot = MBot()
in_msgs = []
out_msgs = []
in_msgs_lock = Lock()
out_msgs_lock = Lock()

def bridge(websocket):
    global in_msgs, out_msgs

    while True:

        try:
            in_msg = websocket.recv(timeout=0.1)
            with in_msgs_lock:
                in_msgs.append(in_msg)
        except TimeoutError as e:
            pass
        except Exception as e:
            break;
        
        with out_msgs_lock:
            if (len(out_msgs) > 0):
                websocket.send(out_msgs.pop(0))
        
def parse_msgs():
    global mbot, msgs
    while True:
        with in_msgs_lock:
            if (len(in_msgs) > 0):
                message = in_msgs.pop(0)
            else:
                continue

        json_data = json.loads(message)
        if (json_data.get('cmd') == "drive"):
            vx = json_data.get('args').get('vx')
            vy = json_data.get('args').get('vy')
            wz = json_data.get('args').get('wz')
            mbot.drive(vx, vy, wz)
            print(json_data.get('args'))
        elif (json_data.get('cmd') == "stop"):
            mbot.stop()
            print("Stopping")
        elif (json_data.get('cmd') == "read_lidar"):
            print("Reading Lidar")
            ranges, thetas = mbot.read_lidar()
            msg = json.dumps({
                                    'ranges': ranges,
                                    'thetas': thetas
                                    }).encode()
            with out_msgs_lock:
                out_msgs.append(msg)
        elif (json_data.get('cmd') == "read_odometry"):
            x, y, theta = mbot.read_odometry()
            print("Reading Odometry")
            client.send(json.dumps({
                                    'x': x,
                                    'y': y,
                                    'theta': theta
                                    }).encode())
        elif (json_data.get('cmd') == "reset_odometry"):
            mbot.reset_odometry()
            print("Resetting Odometry")
        elif (json_data.get('cmd') == "drive_path"):
            path = json_data.get('args').get('path')
            mbot.drive_path(path)
            print("Driving Path")
        elif (json_data.get('cmd') == "read_slam_pose"):
            x, y, theta = mbot.read_slam_pose()
            print("Reading SLAM Pose")
            msg = json.dumps({
                                'x': x,
                                'y': y,
                                'theta': theta
                                }).encode()
            with out_msgs_lock:
                out_msgs.append(msg)
        elif (json_data.get ('cmd') == "read_hostname"):
            hostname = mbot.read_hostname()
            msg = json.dumps({
                                'hostname': hostname
                                }).encode()
            with out_msgs_lock:
                out_msgs.append(msg)
                    
def main():
    parse_thread = Thread(target=parse_msgs, name='parse_thread', daemon=True)
    parse_thread.start()
    with serve(bridge, "localhost", 8765) as server:
        server.serve_forever()

if __name__ == '__main__':
    main()