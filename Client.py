import socket
import signal
import sys
import threading
import psutil
import time
import os


def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)
    

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')


ip_addr = "127.0.0.1"
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip_addr, tcp_port))

        

while True:
    try:
        process = psutil.Process(os.getpid())
        cpuusage = str(psutil.cpu_percent(interval=1))
        memoryusage = str(process.memory_info().rss)
        message = "CPU "+ cpuusage + " RAM " + memoryusage + " bytes"
        sock.send(message.encode())
        response = sock.recv(4096).decode()
        print('Server response: {}'.format(response))
        time.sleep(1)
            
    except (socket.timeout, socket.error):
        print('Server error. Done!')
        sys.exit(0)