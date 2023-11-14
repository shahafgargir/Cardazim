

import argparse
import sys
import struct
import socket
import math

###########################################################
####################### YOUR CODE #########################
###########################################################


def set_server(client_ip, client_port):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind((client_ip, client_port))
    serv.listen(1)
    while True:
        conn, addr = serv.accept()
        from_client = ''
        data_length_binary = conn.recv(4)
        data_length = int.from_bytes(data_length_binary, "little")

        while (len(from_client) < data_length):
            data = conn.recv(4096)
            from_client += data.decode('utf8')

        print ("Received data: ",from_client)
        conn.close()
    print ('client disconnected and shutdown')


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='set server.')
    parser.add_argument('client_ip', type=str,
                        help='the client\'s ip')
    parser.add_argument('client_port', type=int,
                        help='the client\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and receave data from client.
    '''
    args = get_args()
    try:
        set_server(args.client_ip, args.client_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())



