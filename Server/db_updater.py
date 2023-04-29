from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from logging import basicConfig, getLogger, DEBUG
from argparse import ArgumentParser
import json
import mysql.connector

 ## TO-DO: add a response message to let the client know if they need to send again or not. And in client code wrap .close() so that it only runs if return was successfull. 

def update_db(data_list_of_touples):
    # Connect to the database
    db_host = "ipfs-server.mysql.database.azure.com"
    db_user = "mrprcsuoxp"
    db_pass = "pass@cs6675db"
    db_name = "ipfs-db"
    conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)

    # Insert the new keyword into the database
    sql = "INSERT INTO keywords (keyword, cid) VALUES (%s, %s)"
    cursor = conn.cursor()
    cursor.executemany(sql, data_list_of_touples)
    
    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()


def parse_json(json_data):
    logger.info(f"I received this: {json_data}")

    data_dict = json.loads(json_data)
    data_list_of_touples = []

    for keywords in data_dict.keys():
        touple = (keywords, data_dict[keywords][0][0])  ## this is for the easy case, just sending one of the cid's. Maybe we can send all (nested forloop on length data_dict[keywords])
        data_list_of_touples.append(touple)
        
    update_db(data_list_of_touples)


def handle_agent_connections(socket, addr):                                                       
    logger.info(f"Connected with {addr}")

    # Initialize an empty list to store the received chunks of data
    data_chunks = []

    while True:
        request = socket.recv(1024)
        if not request:
            logger.info(f"Closing connection with {addr}")
            break
        else: 
            #logger.info(f"Connected with {addr}")
            data_chunks.append(request)  # Store the received chunk of data

    # Decode and join the data chunks to form the complete JSON data
    complete_data = ''.join(chunk.decode() for chunk in data_chunks)
    
    # Call parse_json with the complete_data
    parse_json(complete_data)
    
    socket.close()
    logger.info("Connection closed: %s", addr)



if __name__ == "__main__":
    # Logger setup
    basicConfig(filename='logs.log', format="%(message)s", filemode="a")
    logger = getLogger()
    logger.setLevel(DEBUG)
    logger.info("Logger activated.")

    # Parsing arguments
    parser = ArgumentParser()
    parser.add_argument('-ip', type=str, help='reachable_ip')
    parser.add_argument('-port_num', type=int, help='transfer-port-num')
    args = parser.parse_args()

    # Socket setup
    serverPort = args.port_num
    serverHost = args.ip
    db_updater_socket = socket(AF_INET, SOCK_STREAM)
    db_updater_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    db_updater_socket.bind((serverHost, serverPort))
    db_updater_socket.listen(20)
    logger.info("Db_updater can now receive connections.")

    # Start receiving connection requests
    while True:
        new_agent_socket, addr = db_updater_socket.accept()
        new_agent_thread = Thread(target=handle_agent_connections, args=(new_agent_socket, addr,))
        new_agent_thread.start()
