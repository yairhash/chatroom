import socket
import threading
import time
from person import Person
from admin import Admin
from persons import persons
from api import receive
from handle_admin import handle_admin
from client import clients

#משתנים קבועים
PORT=5050
HOST=socket.gethostbyname(socket.gethostname())
ADDR =(HOST,PORT)  
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server_socket.bind(ADDR)  
FORMAT='utf-8'
MAX_CONNECTION=10
admin=Admin()





#פונקציה שמטלפת בכל לקוח בנפרד
def handle_client(person):
    while True:
        try:
            msg=message=person.client.recv(1024)
            name_from_the_client=person.client.recv(1204).decode(FORMAT)
            if name_from_the_client=='admin':
                if msg.decode(FORMAT).startswith('KICK'):
                    admin.kick_user(name_from_the_client)
                elif msg.decode(FORMAT).startswith('BAN'):
                    admin.write_to_ban_file(name_from_the_client)
                    admin.kick_user(name_from_the_client) 
                else:
                    person.client.send('Command was refuse'.encode(FORMAT))
            else:
                admin.broadcast(message)       
        except:
            print('An error occurred')
            person.client.close()
            break
          
#הפונקציה מטפלת בחיבורים החדשים ומנווטת אותם למקומות השונים
def start_server(): 
    server_socket.listen(MAX_CONNECTION)
    print(f'[LISTENING]Server is listening on port {PORT}')
    start_communication()


def start_communication():    
    while True:
        try:
            client,address=server_socket.accept()  #הקונקשן יוצר סוקט אובג'קט שבאמצעותו אנו רואים מי התחבר 
            message_to_client=client.send('name'.encode(FORMAT))
            clients(message_to_client)
            
            client_name=receive()
            print(client_name) 
            if client_name!='admin':
                is_ban=admin.check_for_ban(client_name,client)
                if is_ban:
                    client.send(401)
                    client.close()
                else:
                    client.send('connected'.encode(FORMAT))
                               
            else:
                server_socket.send('PASS'.encode(FORMAT))
                handle_admin(server_socket)
                password=receive()
                if password=='adminpass':
                    client.send('connected'.encode(FORMAT))
                else:
                    client.send(401)    
            person=Person(address,client,client_name)
            print(f'Client name is {client_name}')
            print(f'[CONNECTION] {address} connected to the server')
            person.client.send('connected'.encode(FORMAT))
            message=f'{client_name} joined the chat!'.encode(FORMAT)
            admin.broadcast(message)
            persons.append(person)
            thread=threading.Thread(target=handle_client,args=(person,))
            thread.start()
            print(f'ACTIVE CONNECTIONS {threading.activeCount() -1}')                
        except:
            print('An error occurred')



                

print('[STARTING]the Server is starting....')
start_server()        





# #פונקציה שמטלפת בכל לקוח בנפרד
# def handle_client(person):
#     while True:
#         try:
#             msg=message=person.client.recv(1024)
#             name_from_the_client=person.client.recv(1204).decode(FORMAT)
#             if msg.decode(FORMAT).startswith('KICK'):
#                 if name_from_the_client=='admin':
#                     name_to_kick=msg.decode(FORMAT)[5:]
#                     kick_user(name_to_kick)
#                 else:
#                     person.client.send('Command was refuse'.encode(FORMAT))         
#             elif msg.decode(FORMAT).startswith('BAN'):
#                 if person.name=='admin':
#                     name_to_ban=msg.decode(FORMAT)[4:]
#                     kick_user(name_to_ban)
#                     with open('bans.txt','a')as f:
#                         f.write(f'{name_to_ban}\n')
#                     print(f'{name_to_ban} was banned')  
#                 else:
#                     person.client.send('Command was refuse'.encode(FORMAT))  
#             else: 
#                 broadcast(message)
                
#         except:
#             for person in persons:
#                 if person.client in persons:
#                     persons.remove(person)
#                     person.client.close()
#                     broadcast(f'{person.name} left the chat'.encode(FORMAT))
#                     break  



# #הפונקציה מטפלת בחיבורים החדשים ומנווטת אותם למקומות השונים
# def start_server(): 
#     server.listen(MAX_CONNECTION)
#     print(f'[LISTENING]Server is listening on port {PORT}')
#     while True:
#         try:
#             client,address=server.accept()  #הקונקשן יוצר סוקט אובג'קט שבאמצעותו אנו רואים מי התחבר 
#             client.send('name'.encode(FORMAT))
#             client_name=client.recv(1024).decode(FORMAT)
#             person=Person(address,client,client_name)
#             print(f'[CONNECTION] {address} connected to the server')
#             with open('bans.txt','r') as f:
#                 bans=f.readlines()
#             if client_name+'\n' in bans:
#                 client.send('BAN'.encode(FORMAT))
#                 client.close()
#                 continue
#             if client_name=='admin':
#                 client.send('PASS'.encode(FORMAT))
#                 password=client.recv(1024).decode(FORMAT)
#                 if password!='adminpass':
#                     client.send('REFUSE'.encode(FORMAT))
#                     client.close()
#                     continue    # אנחנו לא רוצים לצאת מהלופ כי אנחנו רוצים לנמשיך את ההתחברות של הקליינטים נאחרים , לכן משתמשים ב continue  
#             persons.append(person)
#             print(f'Client name is {client_name}')
#             broadcast(f'{client_name} joined the chat!'.encode(FORMAT))
#             client.send('You connected to the server'.encode(FORMAT))
#             thread=threading.Thread(target=handle_client,args=(person,))
#             thread.start()
#             print(f'ACTIVE CONNECTIONS {threading.activeCount() -1}')
#         except:
#             print('An error occurred')

                
              
# def kick_user(name):
#     print(name)
#     for person in persons:
#         if name in person:
#             person.client.send(f'You were kicked by the admin!'.encode(FORMAT))
#             persons.remove(person)
#             broadcast(f'{name} was kicked by the admin'.encode(FORMAT))
#             person.client.close()
                
        

# print('[STARTING]the Server is starting....')
# start_server()        


