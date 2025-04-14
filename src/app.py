import os
from flask import Flask, render_template, request, redirect, url_for
import conexion as db

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()  # La información viene como tupla y se debe convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

@app.route('/user', methods=['POST'])
def addUser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if name and email and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (name, email, password) VALUES(%s, %s, %s)"
        data = (name, email, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if name and email and password:
        cursor = db.database.cursor()
        sql = "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s"
        data = (name, email, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__=='__main__':
    
    app.run(debug=True, port=4000)