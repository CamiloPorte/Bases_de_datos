from app import app
from flask import render_template,request,redirect
from configuraciones import *
import psycopg2

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,passwd))
cur = conn.cursor()

@app.route('/', methods=["POST", "GET"])
def formulario():
	return render_template("login.html")

@app.route('/login', methods=["POST", "Get"])
def login():

	sql ="""
	SELECT num_mesa,clientes_totales
	From(select SUM(cant_atendida) as clientes_totales,num_mesa
	FROM pedidos
	GROUP BY num_mesa ) as holi
	order by (clientes_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topventa = cur.fetchall()

	sql ="""
	SELECT nombre,apellido,cont
	FROM (select count(fecha,hora) AS cont, nombre, apellido
	FROM pedidos, empleados
	WHERE empleados.rut = pedidos.rut_empleado
	GROUP BY empleados.rut)AS holi
	ORDER BY(cont) DESC;
	"""
	print sql
	cur.execute(sql)
	Top = cur.fetchall()

	sql ="""
	SELECT num_mesa,clientes_totales
	From(select SUM(cant_atendida) as clientes_totales,num_mesa
	FROM pedidos
	GROUP BY num_mesa ) as holi
	order by (clientes_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topprecio = cur.fetchall()

	alerta=""

	sql="""SELECT * from empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	if request.method == "POST":
		rut = request.form["loginrut"]
		password = request.form["loginPassword"]

		sql="""SELECT rut,password from empleados where empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		resultados = cur.fetchone()

		sql="""SELECT admin from empleados where empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		admin = cur.fetchone()

		sql="""SELECT nombre,apellido from empleados where empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		nombre = cur.fetchone()


		if resultados == None	:
			alerta="cuenta inexistente"
			return render_template("login.html", alerta = alerta)

		elif resultados[1] != password :
			alerta="contrasena invalida"
			return render_template("login.html", alerta = alerta )
		else :
			return render_template("tables.html", empleados = empleados , administrador=admin , name = nombre, top = Top, Topventa=Topventa,Topprecio=Topprecio)
	else:

		return render_template("login.html")

@app.route('/registrarse', methods=["POST","GET"])
def registrarse():

	sql="""SELECT nombre,apellido from empleados,pedidos where empleado.rut = pedidos.rut_empleado and count(cant_atendida,fecha_id,rut_empleado,num_mesa,idmenu) group by empleados.rut"""

	sql="""SELECT * from empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql="""SELECT nombre, apellido from empleados"""
	cur.execute(sql)
	nombres = cur.fetchone()
	alerta=""
	if request.method == "POST":
		password=request.form["password"]
		rut=request.form["rut"]
		nombre=request.form["nombre"]
		apellido=request.form["apellido"]

		sql="""SELECT nombre,apellido from empleados where empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		nombre = cur.fetchone()

		print(rut)
		print(rut)
		if len(rut) >10 and len(rut) < 9:
			alerta="Rut invalido vuelva ingresar"
			return render_template("register.html", alerta = alerta)

		sql="""SELECT * from empleados where empleados.rut ='%s';
		"""%(rut)
		cur.execute(sql)
		resultadoempleado = cur.fetchall()
		print(resultadoempleado)

		if len(resultadoempleado) == 0 :
			sql ="""INSERT INTO empleados (rut,nombre,apellido,password,admin) VALUES ('%s','%s','%s','%s',false);
			"""%(rut,nombre,apellido,password)
			cur.execute(sql)

			sql="""SELECT nombre,apellido from empleados where empleados.rut = '%s'
			"""%(rut)
			cur.execute(sql)
			nombre = cur.fetchone()
			conn.commit()
			return render_template("tables.html", empleados = empleados , administrador=admin , name = nombres,alerta = alerta,top=top)

		elif len(resultadoempleado) != 0:
			alerta="Rut ya utilizado"
			return render_template("register.html", alerta = alerta)
		else:
			return render_template("register.html",alerta=alerta)
	else:
		return render_template("register.html",alerta=alerta)


@app.route('/tables',methods=["POST","GET"])
def actualizacion():

	sql ="""
	SELECT nombre,apellido,cont
	FROM (select count(fecha_id) AS cont, nombre, apellido
	FROM pedidos, empleados
	WHERE empleados.rut = pedidos.rut_empleado
	GROUP BY empleados.rut)AS holi
	ORDER BY(cont) DESC;
	"""
	print sql
	cur.execute(sql)
	Top = cur.fetchall()
	return render_template("tables.html",top = Top)

@app.route('/test', methods=["POST","GET"])
def test():
	return render_template("charts.html")
