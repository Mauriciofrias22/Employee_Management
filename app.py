from flask import Flask, request, flash, render_template, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import functools

from db import get_db


app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            db = get_db()
            error = None

            if not username:
                error = 'Debes ingresar un usuario'
                flash(error)
                return render_template('index.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('index.html')

            user = db.execute('SELECT usuario, id_empleado FROM empleados WHERE correo= ? AND contraseña= ?',(username, password)).fetchone()


            if user is None:
                error = 'Usuario o contraseña inválidos'
                flash(error)
            else:
                if user[0] == 1:
                    data=rendervisualf(user)
                    return render_template('VisualizarUsuarioFinal.html', data=data)
                elif user[0] == 2:
                    data=rendervisualf(user)
                    return render_template('gestorEmpleadosAdmin.html', data=data)
                elif user[0] == 3:
                    data=rendervisualf(user)
                    return render_template('gestorUsuarioSuper.html', data=data)
                db.close_db()

        return render_template('index.html')
    except Exception as ex:
        print(ex)
        return render_template('index.html')

def rendervisualf(user):
     lag = user[1]
     dt = get_db()
     data = dt.execute('SELECT nombres , apellidos, documento , des_contrato, fecha_inicio, fecha_final , des_cargo, des_dependencia, Salario  FROM empleados,contrato,cargo,dependencia WHERE id_empleado= ? AND id_contrato=(SELECT cod_tipo_contrato FROM empleados WHERE id_empleado = ?) AND id_cargo = (SELECT cargo FROM empleados WHERE id_empleado = ?) AND id_dependencia = (SELECT dependencia FROM empleados WHERE id_empleado = ?)' , (lag,lag,lag,lag)).fetchone()
     return data

@app.route ('/ver/<doc>')
def renderver(doc):      
     dt = get_db()
     data = dt.execute('SELECT nombres , apellidos, documento , des_contrato, fecha_inicio, fecha_final , des_cargo, des_dependencia, Salario  FROM empleados,contrato,cargo,dependencia WHERE documento= ? AND id_contrato=(SELECT cod_tipo_contrato FROM empleados WHERE documento = ?) AND id_cargo = (SELECT cargo FROM empleados WHERE documento = ?) AND id_dependencia = (SELECT dependencia FROM empleados WHERE documento = ?)' , (doc,doc,doc,doc)).fetchone()
     return render_template('VisualizarUsuarioFinal.html', data=data)  

@app.route('/VisualizadordesdeAdmin', methods=['GET', 'POST'])
def visualizadordesdeAdmin(user):
    data=rendervisualf(user)
    return render_template('VisualizarUsuarioFinal.html', data=data)
    

@app.route('/VisualizarUsuarioSuper', methods=['GET', 'POST'])
def visualizarUsuarioSupe():
    return render_template('VisualizarUsuarioFinal.html')


@app.route('/menu_administrador', methods=['GET', 'POST'])
def menu_administrador():
    data=rendervisualf()
    return render_template('gestorEmpleadosAdmin.html')


@app.route('/AgregarEmpleados', methods=['GET', 'POST'])
def btn_agregarEmpleados():
    try:
        if request.method == 'POST':
            selectIDtype = request.form['selectIDtype']
            selectCargo = request.form['selectCargo']
            selectContractType = request.form['selectContractType']
            selectDependencia = request.form['selectDependencia']
            IDnumber = request.form['IDnumber']
            name = request.form['name']
            lastNames = request.form['lastNames']
            Salary = request.form['Salary']
            fechadeingreso = request.form['fechadeingreso']
            Findelcontrato = request.form['Findelcontrato']
            Mail = request.form['Mail']
            Password = request.form['Password']

            db2 = get_db()
            db2.execute("INSERT INTO empleados (tipo_doc, documento, usuario, nombres, apellidos, salario, cod_tipo_contrato, cargo, dependencia, fecha_inicio, fecha_final, correo, contraseña) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(selectIDtype, IDnumber, 1, name, lastNames, Salary, selectContractType, selectCargo, selectDependencia, fechadeingreso, Findelcontrato, Mail, generate_password_hash(Password)))
            db2.commit()
            usuario_creado = "Usuario Creado Con Exito"
            flash(usuario_creado)
            
    except Exception as ex:
        print(ex)

    return render_template('AgregarEmpleados.html')

@app.route('/PuenteBuscarEmpleados', methods=['GET', 'POST'])
def puentebuscarEmpleados():
    try:
        db = get_db()
        data = db.execute('SELECT * FROM empleados WHERE usuario = 1').fetchall()
    except Exception as ex:
        print(ex)
    return render_template('BuscarEmpleado.html', data = data)

@app.route('/PuenteBuscarUsuario', methods=['GET', 'POST'])
def puentebuscarUsuario():
    try:
        db = get_db()
        data = db.execute('SELECT * FROM empleados WHERE usuario < 3').fetchall()
    except Exception as ex:
        print(ex)
    return render_template('BuscarEliminarUsuario.html', data = data)

@app.route('/EliminarUsuario/<doc>')
def eliminarUsuario(doc):   
    db=get_db()    
    db.execute('DELETE FROM empleados WHERE documento = ?', (doc, ))
    db.commit()
    return redirect(url_for('puentebuscarUsuario'))


@app.route('/BuscarEmpleados', methods=['GET', 'POST'])
def buscarEmpleados():                 
    try: 
        db = get_db
        n = db.execute('SELECT documento FROM empleados').fetchall()
        for i in n:
            data1=[]
            data1.append(db.execute('SELECT nombres , apellidos, desc_documento, documento , des_contrato, fecha_inicio, fecha_final , des_cargo, des_dependencia, Salario  FROM empleados, documento, contrato,cargo,dependencia WHERE documento= ? AND id_contrato=(SELECT cod_tipo_contrato FROM empleados WHERE documento = ?) AND id_cargo = (SELECT cargo FROM empleados WHERE documento = ?) AND id_dependencia = (SELECT dependencia FROM empleados WHERE documento = ?) AND id_doc = (SELECT tipo_doc FROM empleados WHERE documento = ?)' , (i[0], i[0], i[0], i[0], i[0])).fetchone())  
        
    except  Exception as ex:
        print(ex)
    return render_template('BuscarEmpleado.html', data1=data1)
    


@app.route('/EditarEmpleados', methods=['GET', 'POST'])
def editarEmpleados():
    return render_template('EditarEmpleados.html')


@app.route('/DesempeñoEmpleados', methods=['GET', 'POST'])
def desempeñoEmpleados():
    return render_template('DesempeñoEmpleado.html')





@app.route('/menuSuperAdmin', methods=['GET', 'POST'])
def menuSuperAdmin():
    return render_template('gestorUsuarioSuper.html')


@app.route('/AgregarUsuarioSuper', methods=['GET', 'POST'])
def btn_agregarUsuarioSuper():
    try:
        if request.method == 'POST':
            selectIDtype = request.form['selectIDtype']
            selectCargo = request.form['selectCargo']
            selectContractType = request.form['selectContractType']
            selectDependencia = request.form['selectDependencia']
            IDnumber = request.form['IDnumber']
            name = request.form['name']
            lastNames = request.form['lastNames']
            Salary = request.form['Salary']
            fechadeingreso = request.form['fechadeingreso']
            Findelcontrato = request.form['Findelcontrato']
            Mail = request.form['Mail']
            Password = request.form['Password']

            db2 = get_db()
            db2.execute("INSERT INTO empleados (tipo_doc, documento, usuario, nombres, apellidos, salario, cod_tipo_contrato, cargo, dependencia, fecha_inicio, fecha_final, correo, contraseña) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(selectIDtype, IDnumber, 1, name, lastNames, Salary, selectContractType, selectCargo, selectDependencia, fechadeingreso, Findelcontrato, Mail, generate_password_hash(Password)))
            db2.commit()
            usuario_creado = "Usuario Creado Con Exito"
            flash(usuario_creado)
            
    except Exception as ex:
        print(ex)

    return render_template('AgregarUsuario.html')


@app.route('/EditarUsuariosuper', methods=['GET', 'POST'])
def editarUsuariosuper():
    return render_template('EditarUsuarioSuper.html')


@app.route('/BuscaryEliminarUsuario', methods=['GET', 'POST'])
def buscaryEliminarUsuario():
    return render_template('BuscarEliminarUsuario.html')


@app.route('/DesempeñoUsuarioSuper', methods=['GET', 'POST'])
def desempeñoUsuarioSuper():
    return render_template('DesempeñodesdeSuper.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))