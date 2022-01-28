import socket
import signal
import struct
import sys
import psutil
import time
import os
import math


def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)
    

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')


ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))
msg = sock.recv(4096)
ID = struct.unpack('!I',msg)[0]

print("Conected with ID: {}".format(ID))

        

while True:
    try:
        process = psutil.Process(os.getpid())
        cpuusage = int(psutil.cpu_percent(interval=1))
        memoryusage = psutil.virtual_memory().used
        exp = int(len(str(memoryusage)) / 3)
        memoryusage = (float)(memoryusage / math.pow(1024,exp))
        message = struct.pack('!IIf',cpuusage,exp,round(memoryusage,2))
        sock.send(message)
        response = sock.recv(4096).decode()
        print('Server response: {}'.format(response))
        time.sleep(5)
            
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)