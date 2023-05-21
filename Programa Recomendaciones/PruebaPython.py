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
        result = tx.run("MATCH (estudiante:Estudiante {name: 'Gerardo'})-[:Tiene]->(c:Cualidad) WITH estudiante, COLLECT(DISTINCT c) AS estudianteCualidades MATCH (clase:Clase {name: 'Calculo1'})-[:Da]->(profesor:Profesor)-[:Tiene]->(c:Cualidad) WITH estudiante, estudianteCualidades, profesor, COLLECT(DISTINCT c) AS profesorCualidades RETURN estudiante.name AS estudiante, profesor.name AS profesor, SIZE([x IN estudianteCualidades WHERE x IN profesorCualidades]) AS similitud ORDER BY similitud DESC")
        for record in result:
            from_name = record["estudiante"]
            print(from_name)
            to_name = record["profesor"]
            print(to_name)
            similarity = record["similitud"]
            print(similarity)
        return "ya"
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
