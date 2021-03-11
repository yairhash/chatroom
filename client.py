import socket
import threading
PORT=5050
FORMAT='utf-8'
SERVER=socket.gethostbyname(socket.gethostname()) # בגלל שאנחנו רצים על אותה מכונה אז הכתובת אייפי זהה 
ADDR =(SERVER,PORT)  
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client.connect(ADDR)


nickname=input('Choose a nickname:')
if nickname=='admin':
    password=input('Enter password for admin')
    
stop_thread=False   
    
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message_from_server=client.recv(1024).decode(FORMAT)
            if message_from_server=='Nickname':
                client.send(nickname.encode(FORMAT))
                next_message_from_server=client.recv(1024).decode(FORMAT)
                if next_message_from_server=='PASS':
                    client.send(password.encode(FORMAT))
                    if client.recv(1024).decode(FORMAT)=='REFUSE':
                        print('connection was refused , wrong password')
                        stop_thread=True
                elif next_message_from_server=='BAN':
                    print('connection refused because of ban!')
                    client.close()
                    stop_thread=True            
            else:
                print(message_from_server)  
        except:
            print('An error occurred')
            client.close()
            break
        


def write():
    while True:
        if stop_thread:
            break
        try:    
            message_from_client= f"{nickname}: {input('')}"
            if message_from_client[len(nickname)+2:].startswith('/'):    # השורה הזאת מחלקת מתייחסת רק לאינפוט ומבטלת את הניק ניים +2 מתייחס לנקודותיים ולרווח אחרי האינפוט
                if nickname=='admin':
                    if message_from_client[len(nickname)+2:].startswith('/kick'):
                        client.send(f'KICK {message_from_client[len(nickname)+2+6:]}'.encode(FORMAT))
                    elif message_from_client[len(nickname)+2:].startswith('/ban'):
                        client.send(f'BAN {message_from_client[len(nickname)+2+5:]}'.encode(FORMAT))           
                else:
                     print('Commands ca only be executed by admin!')
            else:
                 client.send(message_from_client.encode(FORMAT))
        except:
                print('An error occurred')
                client.close()
                break


receive_thread=threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()


