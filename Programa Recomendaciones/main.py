from flask import Flask, request, render_template, jsonify
from neo4j import GraphDatabase
import json

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
    
    def CallGetClases(self):
        with self.driver.session() as session:
            entrada = session.execute_write(self.getClases)
        return entrada
    
    def callNames(self):
        with self.driver.session() as session:
            entrada = session.execute_write(self.professorsname)
        return entrada

    def callProfesorRecom(self,correo,clase):
        with self.driver.session() as session:
            entrada = session.execute_write(self.profesoresRecomendados, correo, clase)
        return entrada

    def callDescriptionProfessors(self,nombreProfesores):
        with self.driver.session() as session:
            entrada, profesoresDict = session.execute_write(self.getDescription,nombreProfesores)
        return entrada, profesoresDict

    def callCalificarProfesor(self,nombre,calificacion):
        with self.driver.session() as session:
            entrada = session.execute_write(self.calificarProfesor,nombre,calificacion)
        return entrada

    def callBestPuntuation(self):
        with self.driver.session() as session:
            entrada = session.execute_write(self.getBestProfessor)
        return entrada

    
    @staticmethod
    def getBestProfessor(tx):
        result = tx.run('MATCH (n:Profesor) RETURN n.name, n.Descripcion, n.Personasc, n.Puntuacion ORDER BY n.Puntuacion DESC LIMIT 4')
        profesoresDict = {}
        for record in result:
            profedict = {
                "Descripcion":record["n.Descripcion"],
                "Personasc":record["n.Personasc"],
                "Puntuacion":record["n.Puntuacion"]
            }
            profesoresDict[record["n.name"]] = profedict
        return profesoresDict

    @staticmethod
    def getClases(tx):
        result = tx.run('match (n:Clase) return  n.name')
        arrClases = []
        for record in result:
            arrClases.append(record["n.name"])
        return arrClases

    @staticmethod
    def getDescription(tx,nombreProfesores):
        datosProfesores = []
        profesoresDict = {}
        for nombre in nombreProfesores:
            profesor = []
            profedict = {}
            profesor.append(nombre)
            result = tx.run('match (n:Profesor{name: "'+nombre+'" }) return n.Descripcion, n.Personasc, n.Puntuacion')
            for record in result:
                profedict = {
                    "Descripcion":record["n.Descripcion"],
                    "Personasc":record["n.Personasc"],
                    "Puntuacion":record["n.Puntuacion"]
                }
                profesor.append(record["n.Descripcion"])
                profesor.append(record["n.Personasc"])
                profesor.append(record["n.Puntuacion"])
            profesoresDict[nombre] = profedict
            datosProfesores.append(profesor)
        
        return datosProfesores, profesoresDict


    @staticmethod
    def createNewUser(tx,nombre,correo,contra, arrCualidades):
        result = tx.run('create (n:Estudiante{name: "'+nombre+'", correo: "'+correo+'", contra: "'+contra+'"})')

        for x in arrCualidades:
            print(x)
            query = "match (n:Estudiante{ name: '"+nombre+"'}), (c:Cualidad{name:'"+x+"'}) create (n) - [:Tiene]->(c)"
            tx.run(query)

    @staticmethod
    def professorsname(tx):
        result = tx.run('match (n:Profesor) return n.name')
        namesDict = {}
        for record in result:
            namesDict[record["n.name"]] = record["n.name"]
        return namesDict   

    @staticmethod
    def profesoresRecomendados(tx,correo,clase):
        result = tx.run("MATCH (estudiante:Estudiante {correo: '"+correo+"'})-[:Tiene]->(c:Cualidad) WITH estudiante, COLLECT(DISTINCT c) AS estudianteCualidades MATCH (clase:Clase {name: '"+clase+"'})-[:Da]->(profesor:Profesor)-[:Tiene]->(c:Cualidad) WITH estudiante, estudianteCualidades, profesor, COLLECT(DISTINCT c) AS profesorCualidades RETURN estudiante.name AS estudiante, profesor.name AS profesor, SIZE([x IN estudianteCualidades WHERE x IN profesorCualidades]) AS similitud ORDER BY similitud DESC LIMIT 4")
        arrProfesor = []
        for record in result:
            arrAtributos = []
            arrAtributos.append(record["estudiante"])
            arrAtributos.append(record["profesor"])
            arrAtributos.append(record["similitud"])
            arrProfesor.append(arrAtributos)
        return (arrProfesor)
    
    @staticmethod
    def calificarProfesor(tx,nombre,calificacion):
        result = tx.run('match (n:Profesor{name:"'+nombre+'"}) return n.Personasc, n.Puntuacion')
        arrResultados = []
        for record in result:
            arrResultados.append(int(record["n.Personasc"]))
            arrResultados.append(int(record["n.Puntuacion"]))

        if(arrResultados[0] == 0):
            arrResultados[1] = calificacion
        else:
            sum = arrResultados[1] + int(calificacion)
            arrResultados[1] = sum/2

        arrResultados[0]+=1

        result = tx.run('match (n:Profesor{name:"'+nombre+'"}) set n.Personasc='+str(arrResultados[0])+', n.Puntuacion='+str(arrResultados[1]))


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
#path Diego: C:\\Users\\dgv31\\OneDrive\\Documents\\Universidad\\Semestre 3\\estructura de datos\\Proyecto 2\\Programa Recomendaciones
#path Francis: C:\\Users\\fagui\\Documents\\Francis\\2023\\UVG\\Tercer semestre\\Algoritmos\\neo4j\\proyecto-2-xd\\Programa Recomendaciones

app = Flask(__name__,template_folder= 'C:\\Users\\dgv31\\OneDrive\\Documents\\Universidad\\Semestre 3\\estructura de datos\\.proyecto 2 final\\Programa Recomendaciones') #aqui se empieza a crear la aplicacion
BD = Neo4JExample("bolt://localhost:7687", "neo4j", "12345678")
#neo4j,neo4jj

@app.route('/') #se define un temporador para la ruta principal '/login'

def inicio():
    #renderizamos la plantilla, formulario html
    return render_template('index.html')

@app.route('/form2', methods=['POST'])
def Form2():
    return render_template('PrimerIngreso.html')

@app.route('/buscarRecomendacion', methods=['POST'])
def buscarRecomendacion():
    clase = request.form["clase"]
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    arrClases = BD.CallGetClases()
    flagExistencia= False
    for x in arrClases:
        if(clase.lower() == x.lower()):
            flagExistencia = True
            clase = x
        
    if(flagExistencia):
        arrProfesor = BD.callProfesorRecom(nombre, clase)
        nombreProfe = []
        for x in arrProfesor:
            nombreProfe.append(x[1])

        profesor1 = False
        profesor2 = False
        profesor3 = False
        profesor4 = False
        for i in range(len(nombreProfe)):
            if(i == 0):
                profesor1 = True
            elif(i==1):
                profesor2 = True
            elif(i==2):
                profesor3 = True
            elif(i==3):
                profesor4 = True
        #Aqui estan todos los datos de los profesores :)
        datosProfesores, profesoresDict = BD.callDescriptionProfessors(nombreProfe)
        #print(profesoresDict)
        #datosProfesores = json.dumps(profesoresDict)
        #print(datosProfesores)
        #for datos in datosProfesores:
         #   print(datos)
        
        return render_template('BuscarRecomendaciones.html',busqueda = True, nombre = nombre, contrasena = contrasena, datosProfesores=profesoresDict, flagProfesores=True, profesor1=profesor1, profesor2=profesor2,profesor3=profesor3,profesor4=profesor4)

        ss
        #Por el momento y como esta hecha la base de datos solo manda dos profesores porque solo llega a 2
        #return render_template('BuscarRecomendaciones.html',busqueda = True, nombre = nombre, contrasena = contrasena, profe1 = nombreProfe[0], profe2 = nombreProfe[1])
    else:
        return render_template('BuscarRecomendaciones.html',flagError = True, mensaje = "La clase que ingreso no existe", nombre = nombre, contrasena = contrasena)
    

@app.route('/SoloNombresProfesores', methods=['POST'])
def SoloNombresProfesores():
    namesDict = BD.callNames()
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    
    return render_template('Recomendar.html', namesDict = namesDict, nombre = nombre, contrasena = contrasena, primera = True)

@app.route('/NombresProfesores', methods=['POST'])
def NombresProfesores():
    clase = request.form["clase"]
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    arrClases = BD.CallGetClases()
    flagExistencia= False
    for x in arrClases:
        if(clase.lower() == x.lower()):
            flagExistencia = True
            clase = x
        
    if(flagExistencia):
        arrProfesor = BD.callProfesorRecom(nombre, clase)
        nombreProfe = []
        for x in arrProfesor:
            nombreProfe.append(x[1])
        
        #Aqui estan todos los datos de los profesores :)
        datosProfesores, profesoresDict = BD.callDescriptionProfessors(nombreProfe)
                
        return render_template('Recomendar.html',busqueda = True, nombre = nombre, contrasena = contrasena, datosProfesores=profesoresDict, flagProfesores=True)
    else:
        return render_template('BuscarRecomendaciones.html',flagError = True, mensaje = "La clase que ingreso no existe", nombre = nombre, contrasena = contrasena)
    



@app.route('/menu', methods=['POST'])
def menu():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('MenuPrincipal.html', nombre = nombre, contrasena = contrasena)
#app.jinja_env.globals.update(Redireccion1=Redireccion1)
#cambiar
#calificacion
@app.route('/CrearCalificacion', methods=['POST'])
def CrearCalificacion():
    #nombre = request.form['nombre']
    #contrasena = request.form['contrasena']
    maestro = request.form["maestro"]
    estrellas = request.form["estrellas"]    
    BD.callCalificarProfesor(maestro,estrellas)
    #nombre = nombre, contrasena = contrasena,

    return render_template('Recomendar.html', flagPrimeraVista=True)


@app.route('/primeraVista', methods=['POST'])
def primeraVista():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    professorDict = BD.callBestPuntuation()
    profesor1 = True
    profesor2 = True
    profesor3 = True
    profesor4 = True
    return render_template('BuscarRecomendaciones.html',nombre = nombre, contrasena = contrasena, datosProfesores=professorDict, flagProfesores=True, profesor1=profesor1, profesor2=profesor2,profesor3=profesor3,profesor4=profesor4)

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('BuscarRecomendaciones.html', nombre = nombre, contrasena = contrasena, flagPrimeraVista = True)
#cambiar
@app.route('/recomendar', methods=['POST'])
def recomendar():
    nombre = request.form['nombre']
    contrasena = request.form['contrasena']
    return render_template('Recomendar.html', nombre = nombre, contrasena = contrasena, flagPrimeraVista=True)

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


