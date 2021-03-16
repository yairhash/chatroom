FORMAT='utf-8'
from persons import persons



class Admin(): 
    
    def broadcast(self,msg):
        for person in persons:
            client=person.client
            client.send(msg)

    
    def check_for_ban( self,client_name,client):
        with open('bans.txt','r') as f:
            bans=f.readlines()
            if client_name+'\n' in bans:
                return True
            return False
                
    def write_to_ban_file(self,name):
        with open('bans.txt','a')as f:
            f.write(f'{name}\n')
            print(f'{name} was banned')  
    
    
    def kick_user(self,name):
        print(name)
        for person in persons:
            if name in person:
                person.client.send(f'You were kicked by the admin!'.encode(FORMAT))
                persons.remove(person)
                self.broadcast(f'{name} was kicked by the admin'.encode(FORMAT))
                person.client.close()