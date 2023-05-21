from flask import Flask, request, render_template
#Aqui tienen que cambiar a su ruta de la carpeta raíz
app = Flask(__name__,template_folder= 'C:\\xampp\\htdocs\\proyecto-2-xd\\Programa Recomendaciones') #aqui se empieza a crear la aplicacion

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

    #retornamos una respuesta
    return "<h1>binvenido "+ nombre+"</h1>"
    #return render_template('form.html', nombre=nombre, contrasena=contrasena)

    #redireccionar
    #return render_template('index.html', msg='formulario enviado')

if __name__ == '__main__':
    #se inicia la aplicacion en modo debug
    app.run(debug=True)
