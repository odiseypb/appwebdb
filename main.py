from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import  SQLAlchemy
#from flaskext.mysql import MySQL

# This is a sample Python script.
#pip freeze > requirements.txt
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#source ./venv/bin/activate
# par windows env\Scripts\activate
#pip install flask


#mysql = MySQL()

app = Flask(__name__,static_url_path='/static')
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'Odisey123'
#app.config['MYSQL_DATABASE_DB'] = 'db_productos'
#app.config['MYSQL_DATABASE_PORT'] = 3306
#para postgres
#pip install flask_sqlalchemy
#pip install psycopg2-binary #for using postgres
#mysql.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/formulario")
def formulario_html():
    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")

    datos = cursor.fetchall()

    print(datos)
    cursor.close()

    return render_template("formulario.html", lista_productos=datos)

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos(nombre,descripcion, precio ) VALUES (%s,%s,%s)", (nombre, descripcion, precio))
    conn.commit()
    cursor.close()

    return redirect("/formulario")

@app.route("/eliminar_producto/<string:id>")
def eliminar_producto(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos where id={0}".format(id))
    conn.commit()
    cursor.close()

    return redirect("/formulario")

@app.route("/consultar_producto/<id>")
def obtener_producto(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos where id= %s", (id))
    dato=cursor.fetchone()
    print(dato)
    cursor.close()
    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<id>", methods=['POST'])
def editar_producto(id):
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=%s, descripcion=%s, precio=%s WHERE id=%s", (nombre, descripcion, precio, id))
    conn.commit()
    cursor.close()

    return redirect("/formulario")



@app.route("/optimizacion")
def optimizacion():
    return render_template("optimizacion.html")




# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    app.run(port=3000, debug=True)
