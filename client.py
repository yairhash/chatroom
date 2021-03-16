import socket
import threading
from api import receive

PORT=5050
FORMAT='utf-8'
HOST=socket.gethostbyname(socket.gethostname()) # בגלל שאנחנו רצים על אותה מכונה אז הכתובת אייפי זהה 
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
ADDR =(HOST,PORT)


name=input('What is your name:')

stop_thread=False  


def clients(msg):
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            client.connect(ADDR)            
            if msg=='name':
                client.send(name.encode(FORMAT))
                if receive()==401:
                    print('connection refused because of ban!')
                    client.close()
                    stop_thread=True
                elif msg=='connected':
                    print('You are connected!')
                else:
                    client.send(500)
                    stop_thread=True
        except:
            print('An error occurred !!!')
            client.close()
            break
    




 
    



# def write():                     
#     while True:
#         if stop_thread:
#             break
#         try:    
#             message_from_client=f"{name}: {input('')}"
#             if message_from_client[len(name)+2:].startswith('/'):    # השורה הזאת מחלקת מתייחסת רק לאינפוט ומבטלת את הניק ניים +2 מתייחס לנקודותיים ולרווח אחרי האינפוט
#                 if name=='admin':
#                     if message_from_client[len(name)+2:].startswith('/kick'):
#                         client.send(f'KICK {message_from_client[len(name)+2+6:]}'.encode(FORMAT))
#                         client.send(name.encode(FORMAT))
#                     elif message_from_client[len(name)+2:].startswith('/ban'):
#                         client.send(f'BAN {message_from_client[len(name)+2+5:]}'.encode(FORMAT))           
#                         client.send(name.encode(FORMAT))
#                 else:
#                      print('Commands ca only be executed by admin!')
#             else:
#                  client.send(message_from_client.encode(FORMAT))
#         except:
#                 print('An error occurred')
#                 client.close()
#                 break




# write_thread=threading.Thread(target=write)
# write_thread.start()
    
    
    
    
    
    
    
    
    
    
    
    
# def receive():
#     while True:
#         global stop_thread
#         if stop_thread:
#             break
#         try:
#             message_from_server=client.recv(1024).decode(FORMAT)
#             if message_from_server=='name':
#                 client.send(name.encode(FORMAT))
#                 next_message_from_server=client.recv(1024).decode(FORMAT)
#                 if next_message_from_server=='PASS':
#                     client.send(password.encode(FORMAT))
#                     if client.recv(1024).decode(FORMAT)=='REFUSE':
#                         print('connection was refused , wrong password')
#                         stop_thread=True
#                 elif next_message_from_server=='BAN':
#                     print('connection refused because of ban!')
#                     client.close()
#                     stop_thread=True            
#             else:
#                 print(message_from_server)  
#         except:
#             print('An error occurred')
#             client.close()
#             break
        


# def write():                     
#     while True:
#         if stop_thread:
#             break
#         try:    
#             message_from_client=f"{name}: {input('')}"
#             if message_from_client[len(name)+2:].startswith('/'):    # השורה הזאת מחלקת מתייחסת רק לאינפוט ומבטלת את הניק ניים +2 מתייחס לנקודותיים ולרווח אחרי האינפוט
#                 if name=='admin':
#                     if message_from_client[len(name)+2:].startswith('/kick'):
#                         client.send(f'KICK {message_from_client[len(name)+2+6:]}'.encode(FORMAT))
#                         client.send(name.encode(FORMAT))
#                     elif message_from_client[len(name)+2:].startswith('/ban'):
#                         client.send(f'BAN {message_from_client[len(name)+2+5:]}'.encode(FORMAT))           
#                 else:
#                      print('Commands ca only be executed by admin!')
#             else:
#                  client.send(message_from_client.encode(FORMAT))
#         except:
#                 print('An error occurred')
#                 client.close()
#                 break


# receive_thread=threading.Thread(target=receive)
# receive_thread.start()

# write_thread=threading.Thread(target=write)
# write_thread.start()


