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
    
    def callCreateNewUser(self,nombre,correo,contra, arrCualidades):
        with self.driver.session() as session:
            entrada = session.execute_write(self.createNewUser,nombre,correo,contra, arrCualidades)
        return entrada
    
    @staticmethod
    def createNewUser(tx,nombre,correo,contra, arrCualidades):
        result = tx.run('create (n:Estudiante{name: "'+nombre+'", correo: "'+correo+'", contra: "'+contra+'"})')

        for x in arrCualidades:
            print(x)
            query = "match (n:Estudiante{ name: '"+nombre+"'}), (c:Cualidad{name:'"+x+"'}) create (n) - [:Tiene]->(c)"
            tx.run(query)

    
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
#path Gerax: C:\\Users\\USUARIO\\Desktop\\Proyecto2Github\\proyecto-2-xd\\Programa Recomendaciones
#path Angela: C:\\xampp\\htdocs\\proyecto-2-xd\\Programa Recomendaciones
#path Diego: C:\Users\dgv31\OneDrive\Documents\Universidad\Semestre 3\estructura de datos\.proyecto2\Programa Recomendaciones

app = Flask(__name__,template_folder= 'C:\Users\dgv31\OneDrive\Documents\Universidad\Semestre 3\estructura de datos\.proyecto2\Programa Recomendaciones') #aqui se empieza a crear la aplicacion
BD = Neo4JExample("bolt://localhost:7687", "neo4j", "12345678")
#neo4j,neo4j

@app.route('/') #se define un temporador para la ruta principal '/login'

def inicio():
    #renderizamos la plantilla, formulario html
    return render_template('index.html')

@app.route('/form2', methods=['POST'])
def Form2():
    return render_template('PrimerIngreso.html')

#cambiar

@app.route('/menu', methods=['POST'])
def menu():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('MenuPrincipal.html')
#app.jinja_env.globals.update(Redireccion1=Redireccion1)
#cambiar
@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('BuscarRecomendaciones.html')
#cambiar
@app.route('/recomendar', methods=['POST'])
def recomendar():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('Recomendar.html')
#cambiar
@app.route('/index', methods=['POST'])
def index():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('index.html')

@app.route('/registrar',methods=['POST'])
def Registrar():
    arrCualidades = []
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    correo = request.form['correo']

    if(nombre != "" and contrasena != "" and correo != ""):
        if 'cara1' in request.form:
            arrCualidades.append(request.form['cara1'])
        if 'cara2' in request.form:
            arrCualidades.append(request.form['cara2'])
        if 'cara3' in request.form:
            arrCualidades.append(request.form['cara3'])
        if 'cara4' in request.form:
            arrCualidades.append(request.form['cara4'])
        if 'cara5' in request.form:
            arrCualidades.append(request.form['cara5'])
        if 'cara6' in request.form:
            arrCualidades.append(request.form['cara6'])
        if 'cara7' in request.form:
            arrCualidades.append(request.form['cara7'])
        if 'cara8' in request.form:
            arrCualidades.append(request.form['cara8'])

        if(len(arrCualidades)>=3):
            BD.callCreateNewUser(nombre,correo,contrasena, arrCualidades)
            return render_template('MenuPrincipal.html', nombre=nombre, contrasena=contrasena)
        else:
            return render_template('PrimerIngreso.html', flagError = True,mensaje="Seleccione por lo menos 3 cualidades")
    else:
        return render_template('PrimerIngreso.html', flagError = True,mensaje="Complete todos los campos")        


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
        #return "<h1>El usuario ingresado no existe </h1>"
        #return "<div class='alert alert-warning' role='alert'> This is a warning alert with <a href='#' class='alert-link'>an example link</a>. Give it a click if you like.</div>"
        return render_template('index.html', flagError = True,mensaje="El usuario que inteto ingresar no existe")
    else:
        if(ret[0] == nombre and contrasena == ret[1]):
            #Tal ve aqui darle acceso a alguna otra pantalla como un menu
            return render_template('MenuPrincipal.html', nombre=nombre, contrasena=contrasena)
        else:
            return render_template('index.html', flagError = True,mensaje="Contraseña incorrecta")

    #return render_template('form.html', nombre=nombre, contrasena=contrasena)

    #redireccionar
    #return render_template('index.html', msg='formulario enviado')

if __name__ == '__main__':
    #se inicia la aplicacion en modo debug
    app.run(debug=True)


