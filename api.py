FORMAT='utf-8'
import socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 


def receive():
    message_from_server=client.recv(1024).decode(FORMAT)
    return message_from_server
    
        