from flask import Flask, request, render_template
from neo4j import GraphDatabase

class Neo4JExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_Users(self,correo):
        with self.driver.session() as session:
            entrada = session.execute_write(self.showUsers,correo)
        return entrada
    
    @staticmethod
    def showUsers(tx,correo):
        result = tx.run('match (n:Estudiante{correo: "'+correo+'"}) return n.correo, n.contra')
        print(result)
        ret = []
        for record in result:
            ret.append(record["n.correo"])
            ret.append(record["n.contra"])
        if(len(ret) == 0):
            ret.append("No existe")
        return ret



#Aqui tienen que cambiar a su ruta de la carpeta raíz
app = Flask(__name__,template_folder= 'C:\\Users\\USUARIO\\Desktop\\Proyecto2Github\\proyecto-2-xd\\Programa Recomendaciones') #aqui se empieza a crear la aplicacion
BD = Neo4JExample("bolt://localhost:7687", "neo4j", "12345678")
#neo4j,neo4j

@app.route('/') #se define un temporador para la ruta principal '/login'

def inicio():
    #renderizamos la plantilla, formulario html
    return render_template('index.html')


#se define el route con el metodo post
@app.route('/form', methods=['POST'])
def Form():
    #if request.method == 'POST':
    #variable = lo que se manda del formulario
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']

    ret = BD.print_Users(nombre)
    
    if(ret[0] == "No existe"):
        #Aqui se tiene que poner un alert o algo no se como se hace
        return "<h1>El usuario ingresado no existe </h1>"
    else:
        if(ret[0] == nombre and contrasena == ret[1]):
            #Tal ve aqui darle acceso a alguna otra pantalla como un menu
            return "<h1> Credenciales correctas </h1>"
        else:
            return "<h1>Error en el usuario o contraseña </h1>"

    #return render_template('form.html', nombre=nombre, contrasena=contrasena)

    #redireccionar
    #return render_template('index.html', msg='formulario enviado')

if __name__ == '__main__':
    #se inicia la aplicacion en modo debug
    app.run(debug=True)


