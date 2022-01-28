import math
import socket
import struct
import threading
import signal
import sys

METRIC = ["bytes","KB","MB","GB"]

user_id = 0

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')


def handle_client_connection(client_socket,address,user_id,metric): 
    print('Accepted connection from {}:{} \nID:{}'.format(address[0], address[1],user_id))
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                client_socket.close()
            else:
                msg=struct.unpack('!IIf',request)
                cpu_usage = msg[0]
                exp = msg[1]
                memory_usage = msg[2]
                print('Received from {}: cpu: {}% ; memory: {} {}'.format(user_id,cpu_usage,round(memory_usage,2),metric[exp]))
                msg=("Received").encode()
                client_socket.send(msg)
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(user_id))

ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(ip_addr, tcp_port))

while True:
    client_sock, address = server.accept()
    msg = struct.pack('!I',user_id)
    client_sock.send(msg)
    client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address,user_id,METRIC),daemon=True)
    client_handler.start()
    user_id += 1

