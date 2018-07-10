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
	SELECT id_menu
	FROM menus
	;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()

	sql ="""
	SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	GROUP BY num_mesa, hora) as holi
	ORDER BY (clientes_totales) desc;
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales,num_mesa,fecha, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY num_mesa ,fecha,hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topprecio= cur.fetchall()

	sql ="""
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	tophorasing = cur.fetchall()

	alerta=""

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoTotal = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'True'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoFumadores = cur.fetchone()
	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'false'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoNoFumadores = cur.fetchone()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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

		sql="""SELECT rut,password FROM empleados WHERE empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		resultados = cur.fetchone()

		sql="""SELECT admin FROM empleados WHERE empleados.rut = '%s'
		"""%(rut)
		cur.execute(sql)
		admin = cur.fetchone()

		sql="""SELECT nombre,apellido FROM empleados WHERE empleados.rut = '%s'
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
			 numeroClientesfumadores=numeroClientesfumadores,numeroClientesNofumadores=numeroClientesNofumadores,menus = menus)
	else:

		return render_template("login.html")

@app.route('/registrarse', methods=["POST","GET"])
def registrarse():

	sql ="""
	SELECT id_menu
	FROM menus
	;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()

	sql ="""
	SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	GROUP BY num_mesa, hora) as holi
	ORDER BY (clientes_totales) desc;
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales,num_mesa,fecha, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY num_mesa ,fecha,hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topprecio= cur.fetchall()

	sql ="""
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	tophorasing = cur.fetchall()

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoTotal = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'True'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoFumadores = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'false'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoNoFumadores = cur.fetchone()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	AND zona_fumadores = 'True'
	GROUP BY num_mesa, hora) as holi)as preotriano;
	"""
	print sql
	cur.execute(sql)
	numeroClientesfumadores = cur.fetchone()

	print sql
	cur.execute(sql)
	Top = cur.fetchall()


	sql="""SELECT nombre, apellido FROM empleados"""
	cur.execute(sql)
	nombres = cur.fetchone()

	alerta=""
	if request.method == "POST":
		password=request.form["password"]
		rut=request.form["rut"]
		nombre=request.form["nombre"]
		apellido=request.form["apellido"]

		if len(rut) >10 and len(rut) < 9:
			alerta="Rut invalido vuelva ingresar"
			return render_template("register.html", alerta = alerta)

		sql="""SELECT * FROM empleados WHERE empleados.rut ='%s';
		"""%(rut)
		cur.execute(sql)
		resultadoempleado = cur.fetchall()
		print(resultadoempleado)

		if len(resultadoempleado) == 0 :

			sql ="""INSERT INTO empleados (rut,nombre,apellido,password,admin) VALUES ('%s','%s','%s','%s','false');
			"""%(rut,nombre,apellido,password)
			cur.execute(sql)

			sql="""SELECT nombre,apellido FROM empleados WHERE empleados.rut = '%s'
			"""%(rut)
			cur.execute(sql)
			nombre = cur.fetchone()
			conn.commit()

			sql="""SELECT admin FROM empleados WHERE empleados.rut = '%s'
			"""%(rut)
			cur.execute(sql)
			admin = cur.fetchone()

			return render_template("tables.html", empleados = empleados , administrador=admin , name = nombre,
			 top = Top, Topventa=Topventa,Topprecio=Topprecio,tophoras=tophorascompras,
			 tophorasing=tophorasing,topAsistencia=topAsistencia,rut= rut,numeroClientes=numeroClientes,
			 ingresoTotal = ingresoTotal,ingresoFumadores=ingresoFumadores,ingresoNoFumadores=ingresoNoFumadores,
			 numeroClientesfumadores=numeroClientesfumadores,numeroClientesNofumadores=numeroClientesNofumadores ,menus=menus)

		elif len(resultadoempleado) != 0:
			alerta="Rut ya utilizado"
			return render_template("register.html", alerta = alerta)
		else:
			return render_template("register.html",alerta=alerta)
	else:
		return render_template("register.html",alerta=alerta)


@app.route('/tables/<rut>',methods=["POST","GET"])
def home(rut):

	sql="""
	SELECT admin
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	sql="""SELECT * FROM empleados WHERE empleados.rut ='%s';
	"""%(rut)
	cur.execute(sql)
	resultadoempleado = cur.fetchall()
	print(resultadoempleado)

	sql ="""
	SELECT id_menu FROM menus ;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()
	sql ="""
	SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	GROUP BY num_mesa, hora) as holi
	ORDER BY (clientes_totales) desc;
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales,num_mesa,fecha, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY num_mesa ,fecha,hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	Topprecio= cur.fetchall()

	sql ="""
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi
	ORDER BY (valores_totales) desc;
	"""
	print sql
	cur.execute(sql)
	tophorasing = cur.fetchall()

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus
	WHERE pedidos.idmenu = menus.id_menu
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoTotal = cur.fetchone()

	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'True'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoFumadores = cur.fetchone()
	sql ="""
	SELECT SUM(valores_totales)
	FROM (
	SELECT valores_totales,hora
	FROM(select SUM(cant_atendida*menus.precio_menu) as valores_totales, hora
	FROM pedidos,menus,mesas
	WHERE pedidos.idmenu = menus.id_menu
	AND mesas.numero = pedidos.num_mesa
	AND mesas.zona_fumadores = 'false'
	GROUP BY hora) as holi)
	AS titoFernANDes;
	"""
	print sql
	cur.execute(sql)
	ingresoNoFumadores = cur.fetchone()

	sql ="""
	SELECT SUM (clientes_totales)
	FROM ( SELECT num_mesa,clientes_totales
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
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
	FROM(select SUM(capacidad) as clientes_totales,num_mesa
	FROM pedidos , mesas
	WHERE mesas.numero = pedidos.num_mesa
	AND zona_fumadores = 'True'
	GROUP BY num_mesa, hora) as holi)as preotriano;
	"""
	print sql
	cur.execute(sql)
	numeroClientesfumadores = cur.fetchone()

	print sql
	cur.execute(sql)
	Top = cur.fetchall()
	return render_template("tables.html", empleados = empleados , administrador=admin , name = nombre,
	 top = Top, Topventa=Topventa,Topprecio=Topprecio,tophoras=tophorascompras,
	 tophorasing=tophorasing,topAsistencia=topAsistencia,rut= rut,numeroClientes=numeroClientes,
	 ingresoTotal = ingresoTotal,ingresoFumadores=ingresoFumadores,ingresoNoFumadores=ingresoNoFumadores,
	 numeroClientesfumadores=numeroClientesfumadores,numeroClientesNofumadores=numeroClientesNofumadores,resultadoempleado=resultadoempleado
	 ,menus=menus)


@app.route('/busqueda', methods=["POST","GET"])
def busqueda():
	if request.method == "POST":
		fecha=request.form["fecha"]
		hora=request.form["hora"]

		sql="""SELECT *
		FROM reservas
		WHERE reservas.fecha = '%s'
		AND reservas.horas = '%s'
		"""%(fecha,hora)
		cur.execute(sql)
		resultado = cur.fetchall()

	return render_template(resultado=resultado)

@app.route('/mercaderia', methods=["POST","GET"])
def mercaderia():
	if request.method == "POST":

		ano=request.form["ano"]
		mes=request.form["mes"]
		producto=request.form["producto"]
		fecha=ano + '/'+ mes

		sql="""SELECT *
		FROM traen
		WHERE traen.fecha = '%s'
		AND traen.producto = '%s'
		"""%(fecha)
		cur.execute(sql)
		merca = cur.fetchall()

	return render_template(merca=merca)

@app.route('/test/<rut>', methods=["POST","GET"])
def test(rut):

	sql="""
	SELECT admin
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	return render_template("megazord.html",administrador=admin,name = nombre)

@app.route('/ventas/<rut>', methods=["POST","GET"])
def ventas(rut):

	sql ="""
	SELECT id_menu
	FROM menus
	;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql="""
	SELECT admin
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus)

@app.route('/ingreso/<rut>', methods=["POST","GET"])
def ingreso(rut):

	sql ="""
	SELECT id_menu
	FROM menus;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql="""
	SELECT admin
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	aviso1="No se ingreso producto"

	if request.method == "POST":

		fecha=request.form["fecha"]
		hora=request.form["hora"]
		producto=request.form["menu"]
		cantidad=request.form["cantidad"]
		menu=request.form["menu"]
		num_mesa=request.form["mesa"]

		cantidadx = int(cantidad)

		sql="""SELECT *
		FROM menus
		WHERE menus.id_menu = '%s';
		"""%(menu)
		cur.execute(sql)
		menuing = cur.fetchone()

		sql="""SELECT *
		FROM mesas
		WHERE numero = '%s';
		"""%(num_mesa)
		cur.execute(sql)
		mesaing = cur.fetchone()

		sql="""SELECT cantidad, productos.id_producto
		FROM menus,llevan,productos
		WHERE menus.id_menu = '%s'
		AND menus.id_menu = llevan.menu
		AND llevan.producto = productos.id_producto;
		"""%(menu)
		cur.execute(sql)
		stockactual = cur.fetchall()

		if fecha == "" or hora =="" or producto =="" or cantidad =="" or menu =="" or num_mesa =="":
			aviso1="Error, ingreso de datos vacios"
			return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stockactual)
		elif menuing == None :
			aviso1="Menu inexistente"
			return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stockactual)
		elif mesaing == None :
			aviso1="Mesa inexistente"
			return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stockactual)
		else :
			for stock in stockactual:
				algo = int(stock[0])
				if algo < cantidadx :
					aviso1="Fuera de stock"
					return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stock,cantidad=cantidadx)

			for stock in stockactual:
				sql="""UPDATE productos set cantidad ='%s'
				WHERE id_producto = '%s';
				"""%(stock[0] - cantidadx , stock[1])
				cur.execute(sql)

			sql="""INSERT INTO pedidos(cant_atendida , fecha, hora , rut_empleado , num_mesa ,idmenu )
			VALUES ('%s','%s','%s','%s','%s','%s');
			"""%(cantidad,fecha,hora,rut,num_mesa,producto)
			cur.execute(sql)

			aviso1="Venta ingresada"
		return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stockactual)
	return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso1=aviso1,stockactual=stockactual)

@app.route('/reserva/<rut>', methods=["POST","GET"])
def reserva(rut):

	sql ="""
	SELECT id_menu
	FROM menus
	;
	"""
	print sql
	cur.execute(sql)
	menus = cur.fetchall()

	sql="""SELECT * FROM empleados"""
	cur.execute(sql)
	empleados = cur.fetchall()

	sql="""
	SELECT admin
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	admin = cur.fetchone()

	sql="""SELECT nombre,apellido
	FROM empleados
	WHERE empleados.rut = '%s'
	"""%(rut)
	cur.execute(sql)
	nombre = cur.fetchone()

	aviso1="No se ingreso producto"

	if request.method == "POST":

		fecha=request.form["fecha"]
		hora=request.form["hora"]
		mesa=request.form["mesa"]


		sql="""SELECT *
		FROM reservas
		WHERE fecha = '%s'
		AND id_mesa = '%s'
		AND hora = '%s';
		"""%(fecha,mesa,hora)
		cur.execute(sql)
		reservas = cur.fetchone()

		sql="""SELECT *
		FROM reservas
		WHERE id_mesa = '%s';
		"""%(mesa)
		cur.execute(sql)
		mesaing= cur.fetchone()

		aviso2=""

		if fecha == "" or hora =="" or mesa =="" :
			aviso2="Error, ingreso de datos vacios"
			return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso2=aviso2)
		elif mesaing == None :
			aviso2="Mesa inexistente"
			return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso2=aviso2)
		else :
			sql="""INSERT INTO reservas(id_mesa,fecha,hora)
			VALUES ('%s','%s','%s');
			"""%(mesa,fecha,hora)
			cur.execute(sql)

			aviso2="Reserva ingresada"
		return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso2=aviso2)
	return render_template("ventas.html",administrador=admin,name = nombre,rut=rut,empleados=empleados,menus=menus,aviso2=aviso2)
