from neo4j import GraphDatabase
from tkinter import *

class app(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x200")
        self.configure(bg="blueviolet")
        Button(text="ver",command=self.showUsers).place(x=0,y=5)
        Button(text="Crear",command=self.createUser).place(x=0,y=45)
        self.c1 = Entry(); self.c1.place(x=100,y=45)

        self.BD = Neo4JExample("bolt://localhost:7687", "neo4j", "12345678")

    def showUsers(self):
       self.BD.print_Users()

    def createUser(self):
        self.BD.print_Create(str(self.c1.get()))



class Neo4JExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_Users(self):
        with self.driver.session() as session:
            greeting = session.execute_write(self.showUsers)
            print(greeting)
    
    def print_Create(self, name):
         with self.driver.session() as session:
            greeting = session.execute_write(self.createUsers,name)
            print(greeting)

    @staticmethod
    def showUsers(tx):
        result = tx.run("match (u:Usuario) return u.name")
        return [record['u.name'] for record in result]
        #return result.single()[0]
    
    @staticmethod
    def createUsers(tx,toCreate):
        result = tx.run("create (u:Usuario{name:'"+toCreate+"'}) return u.name")
        return result.single()[0]


'''if __name__ == "__main__":
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "12345678")
    greeter.print_greeting("hello, world")
    greeter.close()'''

bucle = app()
bucle.mainloop()
