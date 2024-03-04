
from threading import Thread
import argparse
import sys
from listener import *
from connection import *

###########################################################
####################### YOUR CODE #########################
###########################################################

def handle_connection(conn : Connection):
    """
    This function gets connected socket and receive 
    the length of it (4 bytes, little endial number) and 
    then the message itself 
    
    :param connect_socket: this is the connected socket we will read from
    :type connect_socket: socket
    :returns: nothing
    :rtype: void
    """
    from_client = conn.receive_message()
    
    print ("Received data: ",from_client)
    conn.send_message("Got Message!")

def set_server(server_ip, server_port):
    """ 
    This function gets the ip and the port that the 
    serverl will listening to, and when accept a connction
    create new tread to handle the connenction and repeate
    the listening untill Ctrl+C 
    
    :param server_ip: the ip we will listening from
    :type server_ip: string
    :param server_port: the port the server will listening to
    :type server_port: int
    :returns: this function run till Ctrl+C
    :rtype: void
    """
    with Listener(server_port,server_ip) as ls:
        with ls.accept() as conn:
            handle_connection(conn)
            # Thread(target=handle_connection, args=[conn]).run()



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



