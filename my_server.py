
import socket
import threading
import time
#משתנים קבועים
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR =(SERVER,PORT)  
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server.bind(ADDR) 
FORMAT='utf-8'
MAX_CONNECTION=10


clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)


#פונקציה שמטלפת בכל לקוח בנפרד
def handle_client(client):
    while True:
        try:
            msg=message=client.recv(1024)
            if msg.decode(FORMAT).startswith('KICK'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_kick=msg.decode(FORMAT)[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refuse'.encode(FORMAT))         
            elif msg.decode(FORMAT).startswith('BAN'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_ban=msg.decode(FORMAT)[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a')as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned')  
                else:
                    client.send('Command was refuse'.encode(FORMAT))  
            else: 
                broadcast(message)
        except:
            if client in clients:
                client_index=clients.index(client)
                clients.remove(client)
                client.close()
                nickname=nicknames[client_index]
                broadcast(f'{nickname} left the chat'.encode(FORMAT))
                nicknames.remove(nickname)  
                break  



#הפונקציה מטפלת בחיבורים החדשים ומנווטת אותם למקומות השונים
def receive(): 
    server.listen(MAX_CONNECTION)
    print(f'[LISTENING]Server is listening on port {PORT}')
    while True:
        client,address=server.accept()  #הקונקשן יוצר סוקט אובג'קט שבאמצעותו אנו רואים מי התחבר 
        print(f'[CONNECTION] {address} connected to the server')
        client.send('Nickname'.encode(FORMAT))
        nickname=client.recv(1024).decode(FORMAT)
        with open('bans.txt','r') as f:
            bans=f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode(FORMAT))
            client.close()
            continue
        if nickname=='admin':
            client.send('PASS'.encode(FORMAT))
            password=client.recv(1024).decode(FORMAT)
            if password!='adminpass':
                client.send('REFUSE'.encode(FORMAT))
                client.close()
                continue    # אנחנו לא רוצים לצאת מהלופ כי אנחנו רוצים לנמשיך את ההתחברות של הקליינטים נאחרים , לכן משתמשים ב continue  
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode(FORMAT))
        client.send('connected to the server'.encode(FORMAT))
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()
        print(f'ACTIVE CONNECTIONS {threading.activeCount() -1}')
        
        
        
        
def kick_user(name):
    if name in nicknames:
        name_index=nicknames.index(name)
        client_to_kick=clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send(f'You were kicked by the admin!'.encode(FORMAT))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by the admin'.encode(FORMAT))
                
        

print('[STARTING]the Server is starting....')
receive()        


