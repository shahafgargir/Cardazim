import struct
import socket
import connection

class Listener:

    def __init__(self, port, host, backlog=100) -> None:
        self.port = port
        self.host = host
        self.backlog = backlog 
        
    def __repr__(self) -> str:
        return "Listener(Port="+str(self.port)+", host=" + str(self.host) + ", backlog=" + str(self.backlog) + ")"
    
    def start(self):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv.bind((self.host, self.port))
        serv.listen(2)

        self.serv = serv
    
    def stop(self):
        self.serv.close

    def accept(self):
        conn, addr = self.serv.accept()
        return connection.Connection(conn)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()



