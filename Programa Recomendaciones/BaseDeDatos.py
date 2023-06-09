from neo4j import GraphDatabase
from tkinter import *
import csv


class app(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Exportar e importar")
        self.geometry("250x100")
        self.configure(bg="blueviolet")
        #Button(text="ver",command=self.showUsers).place(x=0,y=5)
        # bgcolor="#e4c1f9"
        self.btn1 = Button(text="Exportar a csv",command=self.createUser, width=20);self.btn1.place(x=50,y=10); self.btn1.config(bg="#e4c1f9")
        self.btn2 = Button(text="Importar csv a neo4j",command=self.poner, width=20);self.btn2.place(x=50,y=40);self.btn2.config(bg="#e0aaff")
        self.BD = Neo4JExample("bolt://localhost:7687", "neo4j", "12345678")

    def poner(self):
        self.BD.ponerEnNeo()
    def showUsers(self):
       self.BD.print_Users()

    def createUser(self):
        self.BD.crearCSV()



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
        

    def ponerEnNeo(self):
        with open("nodes.csv", mode="r") as file:
            node_reader = csv.DictReader(file)
            nodes = list(node_reader)

# Read relationships from CSV
        with open("relationships.csv", mode="r") as file:
            relationship_reader = csv.DictReader(file)
            relationships = list(relationship_reader)

        with self.driver.session() as session:
                query = "match (n) detach delete n"
                session.run(query)

        with self.driver.session() as session:
            for node in nodes:
                labels = node["labels"]
                labels = labels.replace("[","")
                labels = labels.replace("]","")
                labels = labels.replace("'","")
                properties = node["properties"]
                properties = properties.replace("{","")
                properties = properties.replace("}","")
                proplist = properties.split(",")
                cont = 0
                newProperties = "{"
                for x in proplist:
                    proplist2 = x.split(":")
                    prop = proplist2[0]
                    prop = prop.replace("'","")
                    newProperties+=prop+":"+proplist2[1]
                    if(cont < (len(proplist)-1)):
                        newProperties+=", "
                    cont+=1
                newProperties+="}"

                query = "CREATE (n:{}) SET n = {}".format(labels, newProperties)
                print(query)
                #print(query)
                session.run(query)

        with self.driver.session() as session:
            for relationship in relationships:
                start_node_id = relationship["start_node_id"]
                end_node_id = relationship["end_node_id"]
                relationship_type = relationship["type"]

                query = "MATCH (a), (b) WHERE ID(a) = {} AND ID(b) = {} CREATE (a)-[:{}]->(b)".format(
                    start_node_id, end_node_id, relationship_type
                )
                print(query)
                session.run(query)
        
        print("Termino de ingresar datos")

    def crearCSV(self):
        with self.driver.session() as session:
    # Export nodes
            nodes = session.run("MATCH (n) RETURN n").value()
            with open("nodes.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["node_id", "labels", "properties"])
                for node in nodes:
                    writer.writerow([node.id, list(node.labels), dict(node.items())])

            # Export relationships
            relationships = session.run("MATCH ()-[r]->() RETURN r").value()
            with open("relationships.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["relationship_id", "start_node_id", "end_node_id", "type", "properties"])
                for relationship in relationships:
                    writer.writerow([relationship.id, relationship.start_node.id, relationship.end_node.id, relationship.type, dict(relationship.items())])

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
