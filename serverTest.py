import socket
import json

def main():
    # Create a socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to the address and port
    server.bind(('localhost', 1234))

    # Listen for incoming connections
    server.listen(5)

    # Accept the connection
    client, address = server.accept()

    mbot = MBot()

    # Receive data from the client
    while True:
        data = client.recv(1024)
        json_data = json.loads(data.decode())
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
            client.send(json.dumps({
                                    'ranges': ranges,
                                    'thetas': thetas
                                    }).encode())
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
            client.send(json.dumps({
                                    'x': x,
                                    'y': y,
                                    'theta': theta
                                    }).encode())
        elif (json_data.get ('cmd') == "read_hostname"):
            hostname = mbot.read_hostname()
            client.send(json.dumps({
                                    'hostname': hostname
                                    }).encode())
            
    # Close the connection
    client.close()

if __name__ == '__main__':
    main()