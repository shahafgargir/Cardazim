
from threading import Thread
import argparse
import sys
from listener import *
from connection import *
import card
from saver import Saver

###########################################################
####################### YOUR CODE #########################
###########################################################

def handle_connection(conn : Connection, save_path : str):
    """
    This function gets connected socket and receive 
    the length of it (4 bytes, little endial number) and 
    then the message itself 
    
    :param connect_socket: this is the connected socket we will read from
    :type connect_socket: socket
    :param server_port: the path to save the card
    :type server_port: string
    :returns: nothing
    :rtype: void
    """
    data = conn.receive_message()
    client_card = card.Card.deserialize(data)
    saver = Saver()
    saver.save(client_card, save_path)
    

def set_server(server_ip, server_port, save_path):
    """ 
    This function gets the ip and the port that the 
    serverl will listening to, and when accept a connction
    create new tread to handle the connenction and repeate
    the listening untill Ctrl+C 
    
    :param server_ip: the ip we will listening from
    :type server_ip: string
    :param server_port: the port the server will listening to
    :type server_port: int
    :param server_port: the path to save the card
    :type server_port: string
    :returns: this function run till Ctrl+C
    :rtype: void
    """

    with Listener(server_port,server_ip) as ls:
        while True:
            with ls.accept() as conn:
                handle_connection(conn, save_path)
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
    parser.add_argument('save_path', type=str,
                        help='path for saving the card')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and receave data from client.
    '''
    args = get_args()
    
    set_server(args.client_ip, args.client_port, args.save_path)
    print('Done.')
    # try:
    #     set_server(args.client_ip, args.client_port, args.save_path)
    #     print('Done.')
    # except Exception as error:
    #     print(f'ERROR: {error}')
    #     return 1


if __name__ == '__main__':
    sys.exit(main())



