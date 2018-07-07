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
	From(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	GROUP BY num_mesa, hora) as holi
	order by (clientes_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topventa = cur.fetchall()

	sql ="""
	SELECT hora,cont
	FROM (select COUNT( DISTINCT rut_empleado) AS cont, hora
	FROM pedidos
	GROUP BY hora)AS holi
	ORDER BY(cont) DESC;
	"""
	print sql
	cur.execute(sql)
	tophorascompras = cur.fetchall()

	sql ="""
	SELECT nombre,apellido,cont
	FROM (select count(hora) AS cont, nombre, apellido
	FROM pedidos, empleados
	WHERE empleados.rut = pedidos.rut_empleado
	GROUP BY empleados.rut,fecha,hora)AS holi
	ORDER BY(cont) DESC;
	"""
	print sql
	cur.execute(sql)
	Top = cur.fetchall()

	sql ="""
	SELECT nombre,apellido,cont
	FROM (select count(DISTINCT fecha) AS cont, nombre, apellido
	FROM pedidos, empleados
	WHERE empleados.rut = pedidos.rut_empleado
	GROUP BY empleados.rut,fecha)AS holi
	ORDER BY(cont) DESC;
	"""
	print sql
	cur.execute(sql)
	topAsistencia = cur.fetchall()

	sql ="""
	SELECT num_mesa,valores_totales,fecha,hora
	From(select SUM(cant_atendida*menus.precio_menu) as valores_totales,num_mesa,fecha, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY num_mesa ,fecha,hora) as holi
	order by (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topprecio= cur.fetchall()

	sql ="""
	SELECT valores_totales,hora
	From(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi
	order by (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	tophorasing = cur.fetchall()

	alerta=""

	sql="""SELECT * from empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	From(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	GROUP BY num_mesa, hora) as holi)as preotriano;
	"""
	print sql
	cur.execute(sql)
	numeroClientes = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	From(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi)
	AS titoFernandes;
	"""
	print sql
	cur.execute(sql)
	ingresoTotal = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	From(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	and mesas.zona_fumadores = 'True'
	GROUP BY hora) as holi)
	AS titoFernandes;
	"""
	print sql
	cur.execute(sql)
	ingresoFumadores = cur.fetchone()
	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	From(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	and mesas.zona_fumadores = 'false'
	GROUP BY hora) as holi)
	AS titoFernandes;
	"""
	print sql
	cur.execute(sql)
	ingresoNoFumadores = cur.fetchone()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	From(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	AND zona_fumadores = 'false'
	GROUP BY num_mesa, hora) as holi)as preotriano;
	"""
	print sql
	cur.execute(sql)
	numeroClientesNofumadores = cur.fetchone()


	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	From(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	AND zona_fumadores = 'True'
	GROUP BY num_mesa, hora) as holi)as preotriano;
	"""
	print sql
	cur.execute(sql)
	numeroClientesfumadores = cur.fetchone()

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
			return render_template("tables.html", empleados = empleados , administrador=admin , name = nombre,
			 top = Top, Topventa=Topventa,Topprecio=Topprecio,tophoras=tophorascompras,
			 tophorasing=tophorasing,topAsistencia=topAsistencia,rut= rut,numeroClientes=numeroClientes,
			 ingresoTotal = ingresoTotal,ingresoFumadores=ingresoFumadores,ingresoNoFumadores=ingresoNoFumadores,
			 numeroClientesfumadores=numeroClientesfumadores,numeroClientesNofumadores=numeroClientesNofumadores)
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

@app.route('/test/<rut>', methods=["POST","GET"])
def test(rut):

	sql="""
	SELECT admin
	from empleados
	where empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	from empleados
	where empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	return render_template("forms.html",administrador=admin,name = nombre)
