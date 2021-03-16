import pymongo
from pymongo import MongoClient
cluster=MongoClient('mongodb+srv://root:root@cluster0.ykasy.mongodb.net/test')
db=cluster['ChatMembers']
collection=db['personal_info']
from passlib.hash import pbkdf2_sha256

class Db(): 
    def insert_to_db(self,user):
        existing_user=collection.find_one({'email':user.email})
        if existing_user is None:
            password_encrypted=pbkdf2_sha256.encrypt(user.password)
            collection.insert_one({'_id':user._id,'name':user.name,'age':user.age,'email':user.email,'password':password_encrypted})
            return user['_id'],user['name'],user['age'],user['email'],user['password']
        return False
    
    def get_user_from_db(self,email):
        user=collection.find_one({'email':email}) 
        if user:
            return user['_id'],user['name'],user['age'],user['email'],user['password']
        return False
    
    
    
    def check_user_exist(self,email):
        user=collection.find_one({'email':email})
        if user:
            answer='user_exist'
            return answer
        
    
    
    
    # def update_record(self,online_user):
    #     user=collection.find_one({'_id':online_user._id})
    #     if user:
    #         myquery ={"_id":online_user._id}
    #         newvalues ={ "$set":{ "wins":online_user.wins}}
    #         newvalues1 ={ "$set":{ "losts":online_user.losts}}
    #         collection.update_one(myquery,newvalues)
    #         collection.update_one(myquery,newvalues1)
    #     return 'something went wrong'
          
    # def get_top_five(self):
    #     position=1
    #     li=[]
    #     users=collection.find().sort('wins',-1).limit(5)
    #     for doc in users:
    #         li.append((position,doc['name'],doc['wins']))
    #         position=position+1
    #     return li
     
    # def get_my_ranking(self,online_user):
    #     position=1
    #     li=[]
    #     users=collection.find().sort('wins',-1)
    #     for doc in users:
    #         if online_user.email==doc['email']:
    #             li.append((position,doc['name'],doc['wins']))
    #         else:
    #             position=position+1
    #     return li
                
                 
           
            
        
               
       
 
        
             
        
        
