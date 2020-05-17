'''
Created on May 17, 2020

@author: justin
'''

import socket


def get_port():
    """
    starts scanning to find an available port
    """
    start_port = 9000
    end_port = 10000
    
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock.connect_ex returns 0 on connection
            # so we look for res != 0 
            res = sock.connect_ex(('localhost', port))
            if res != 0:
                return port


if __name__ == '__main__':
    print(get_port())