import argparse
import sys
from  connection import *

###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).

    :param server_ip: the Ip of the server
    :type server_ip: string
    :param server_port: the port we will send the message to
    :type server_port: int
    :returns: nothing
    :rtype: void
    '''
    with Connection.connect(server_ip,server_port) as conn:
        conn.send_message(data)
        from_server = conn.receive_message()
        print (from_server)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
