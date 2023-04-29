import socket
import argparse
import json
import logging


if __name__ == "__main__":

    # Arguments Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-json_path', type=str, help='JSON file path')
    args = parser.parse_args()

    serverName = 'localhost'
    serverPort = 5100
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((serverName, serverPort))

    # Reading and sending the JSON file
    with open(args.json_path, 'r') as json_file:
        data = json_file.read()
        serverSocket.sendall(data.encode())

    # Emptying the JSON file
    with open(args.json_path, 'w') as json_file:
        json_file.write(json.dumps({}))  # Use '[]' for an empty list instead of '{}' for an empty object if needed

    serverSocket.close()
