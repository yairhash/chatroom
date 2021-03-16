class Person():
    def __init__(self,address,client,name):
        self.address=address
        self.client=client
        self.name=None
        
        
        
        
    def __repr__(self):
        return f'Person {self.address},{self.name}'