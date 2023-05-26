# proyecto-2-xd
- Gerardo Pineda - 22880
- Francis Aguilar - 22243
- Fernando Echeverría - 22610
- Diego García - 22404
- Angela García -22869

# ANTES DE CORRER EL PROGRAMA
## Primero Parte: Descargar Las librerias necesarias

Descargar las siguientes librerias para poder empezar a usar el programa

```diff 
+ pip install flask 
 ```
 ```diff 
+ pip install neo4j
 ```
## Segunda Parte: Ingreso de datos a la base de datos
- Primero:


Una vez instalado las librerias digerise a la base de datos neo4j y realizar el siguiente comando
```diff 
+ Match (n) detach delete n
 ```
  Esto es solo para asegurar que no existe nada en la base de datos
 
 - Segundo:

Ejecutar el archivo
 ```diff 
- BaseDeDatos.py
 ```
 Una vez compilado el codigo saldra una pantalla que tiene dos opciones
 
 Apachar el boton que dice importar CSV
<p align="center" width="100%">
    <img width="33%" src="https://github.com/angelargd8/proyecto-2-xd/blob/main/assets/BaseDeDatos2.png"> 
</p>

Una vez dentro verificar que si se haya creado correctamente, si no repetir proceso.

La BD tiene que verse de la siguiente forma:

<p align="center" width="100%">
    <img width="33%" src="https://github.com/angelargd8/proyecto-2-xd/blob/main/assets/BD.png"> 
</p>


## Tercera Parte: Accionar el servido para la interaccion de python a html

Ejectutar el programa de python con el nombre
```diff 
- Main.py
 ```
 
 Deberia de salir algo parecido a esto
 
 <p align="center" width="100%">
    <img width="33%" src="https://github.com/angelargd8/proyecto-2-xd/blob/main/assets/serverPython.png"> 
</p>
 
 Listo! Ahora solo colocar el puerto que ha salido en main.py en la barra de busqueda de cualquier buscador
 
 

## Posibles Errores
 
### <ins> Main.py no se puede accionar </ins>


El error mas comun que sucede a la hora de activar el servidor de python y neo4j es que los dos se crean en el mismo puerto.
para poder solucionar esto es de la siguiente forma.

#### 1) Apague la BD de neo4j
#### 2) Una vez apagada inicie el programa de Main.py (Esto deberia de correr sin ningun problema)
#### 3) Inicie la BD de neo4j (Deberia de aparecer lo que se ve en la imagen


<p align="center" width="100%">
    <img width="33%" src="https://github.com/angelargd8/proyecto-2-xd/blob/main/assets/error.png"> 
</p>


#### 3) Apache el boton azul de abajo a la derecha, esto deberia de cambiar el puerto en el que se despliega el servidor de neo4j.



