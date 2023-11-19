
from threading import Thread
import argparse
import sys
import struct
import socket
import math

###########################################################
####################### YOUR CODE #########################
###########################################################

def handle_connection(connect_socket):
    """
    This function gets connected socket and receive 
    the length of it (4 bytes, little endial number) and 
    then the message itself 
    
    :param connect_socket: this is the connected socket we will read from
    :type connect_socket: socket
    :returns: nothing
    :rtype: void
    """
    from_client = b''
    data_length = 4
    data_length_binary = b''

    #get the length of the sentence 
    while (len(data_length_binary) < data_length):
        data = connect_socket.recv(data_length - len(data_length_binary))
        data_length_binary += data

    data_length = int.from_bytes(data_length_binary, "little")

    #get the sentence itself
    while (len(from_client) < data_length):
        data = connect_socket.recv(min(4096,data_length - len(from_client)))
        from_client += data

    from_client = from_client.decode('utf8')

    print ("Received data: ",from_client)
    connect_socket.close()

def set_server(server_ip, server_port):
    """ 
    This function gets the ip and the port that the 
    serverl will listening to, and when accept a connction
    create new tread to handle the connenction and repeate
    the listening untill Ctrl+C 
    
    :param client_ip: the ip 
    """
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind((server_ip, server_port))
    serv.listen(2)
    while True:
        conn, addr = serv.accept()
        Thread(target=handle_connection, args=[conn]).run()



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



