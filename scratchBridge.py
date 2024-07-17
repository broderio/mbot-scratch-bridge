from websockets.sync.server import serve
from websockets.exceptions import ConnectionClosedError
from threading import Thread, Lock
import json
from mbot_bridge.api import MBot
import time

from camera import CameraHandler

import os
from PIL import Image
import numpy as np
from joblib import dump, load

PATH_TO_MODEL = "two_layer_nn.joblib"

mbot = MBot()
in_msgs = []
out_msgs = []
in_msgs_lock = Lock()
out_msgs_lock = Lock()
isConnected = False

def bridge(websocket):
    global in_msgs, out_msgs, isConnected

    isConnected = True


    while True:

        try:
            in_msg = websocket.recv(timeout=0.01)
            with in_msgs_lock:
                in_msgs.append(in_msg)
        except TimeoutError as e:
            pass
        except Exception as e:
            break;
        
        with out_msgs_lock:
            if (len(out_msgs) > 0):
                websocket.send(out_msgs.pop(0))

    isConnected = False


def parse_json_msg(message):
    global mbot

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
    elif (json_data.get('cmd') == "reset_odometry"):
        mbot.reset_odometry()
        print("Resetting Odometry")
    elif (json_data.get('cmd') == "drive_path"):
        path = json_data.get('args').get('path')
        mbot.drive_path(path)
        
def parse_msgs():
    global mbot, in_msgs, out_msgs, isConnected

    clf = load(PATH_TO_MODEL)

    camera = CameraHandler()

    start_time = time.time()
    while True:
        if not isConnected:
            time.sleep(0.25)
            continue

        with in_msgs_lock:
            if (len(in_msgs) > 0):
                message = in_msgs.pop(0)
                parse_json_msg(message)
        
        if (time.time() - start_time) > 0.1:
            start_time = time.time()
            ranges, thetas = mbot.read_lidar()
            x, y, theta = mbot.read_odometry()
            img = camera.get_processed_image(save=False)
            data = np.asarray(img).reshape(1, -1)
            pred = clf.predict(data)[0]
            msg = json.dumps({
                                'pose': {
                                    'x': x,
                                    'y': y,
                                    'theta': theta
                                },
                                'scan': {
                                    'ranges': ranges,
                                    'thetas': thetas
                                },
                                'prediction': pred 
                                })
            with out_msgs_lock:
                out_msgs.append(msg)
                    
def main():
    parse_thread = Thread(target=parse_msgs, name='parse_thread', daemon=True)
    parse_thread.start()
    with serve(bridge, "0.0.0.0", 8765) as server:
        server.serve_forever()

if __name__ == '__main__':
    main()