from api import receive
import threading
FORMAT='utf-8'
import socket


PORT=5050
FORMAT='utf-8'
HOST=socket.gethostbyname(socket.gethostname()) # בגלל שאנחנו רצים על אותה מכונה אז הכתובת אייפי זהה 
ADDR =(HOST,PORT)


stop_thread=False

def handle_admin(admin):
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            admin.connect(ADDR)
            if receive()=='PASS':
                password=input('Enter password for admin:')
                admin.send(password.encode(FORMAT))
                if receive()==401:
                    print('connection was refused , wrong password')
                    stop_thread=True
                elif receive()=='conneted':
                    print('connected')
        except:
            print('An error occurred !!!')
            admin.close()
            break