import argparse
import sys
from  connection import *
import card

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


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send Card to server.')
    parser.add_argument('card_name', type=str,
                        help='the Card\'s name')
    parser.add_argument('creator_name', type=str,
                        help='the creator\'s name')
    parser.add_argument('riddle', type=str,
                        help='the riddle')
    parser.add_argument('solution', type=str,
                        help='the solution')
    parser.add_argument('path', type=str,
                        help='the path to the image')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        client_card = card.Card.create_from_path(args.card_name, args.creator_name, args.path, args.riddle, args.solution)
        client_card.encript_card()
        data = client_card.serialize()

        send_data("127.0.0.1", 8080, data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
