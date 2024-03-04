import struct
import socket
class Connection:

    @classmethod
    def connect(cls, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host,port))
        return cls(conn)

    def __init__(self, socket) -> None:
        self.socket = socket
    def __repr__(self) -> str:
        return_str = ""
        my_addr = self.socket.getsockname()
        other_addr = self.socket.getpeername()
        return "<Connection from " + my_addr[0] + ":" + str(my_addr[1]) + " to " + other_addr[0]+":" + str(other_addr[1])+ ">"
    def send_message(self, message):
        length = struct.pack("<I",len(message.encode()))
        self.socket.sendall(length + message.encode())
    def receive_message(self):
        message = b''
        data_length = 4
        data_length_binary = b''

        #get the length of the sentence 
        while (len(data_length_binary) < data_length):
            data = self.socket.recv(data_length - len(data_length_binary))
            data_length_binary += data

        data_length = int.from_bytes(data_length_binary, "little")

        #get the sentence itself
        while (len(message) < data_length):
            data = self.socket.recv(min(4096,data_length - len(message)))
            message += data
            if (len(data)== 0):
                raise ConnectionAbortedError

        return message.decode('utf8')
    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()



