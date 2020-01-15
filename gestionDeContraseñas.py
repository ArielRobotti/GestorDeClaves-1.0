'''Este proyecto consiste, por el momento, en una interface 
gráfica para la manipulación y resguardado de contraseñas '''
from random import *
from tkinter import * 
from functools import * 
from claseContr import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb 
from encriptar import*

raiz=Tk()
raiz.geometry("600x290")
raiz.title("KeyGest 1.0")
raiz.iconbitmap("llaves.ico")
raiz.resizable(0,0)

Fuente=("Arial",14)

barraBuscar=Frame(raiz)
barraBuscar.grid(row=7,column=1,columnspan=4,padx=2,pady=6)

resultados=[]
grupo=[]
archivoActivo=None
registroActivo=None
indiceRegAct=None

varUrl=StringVar()
varEmail=StringVar()
varContraseña=StringVar()
varUsuario=StringVar()
varObserv=StringVar()
info=StringVar()

barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)
def nuevo():
	global grupo
	global archivoActivo
	if archivoActivo==None:
		grupo=[]
		raiz.title("KeyGest 1.0	"+"...........Nuevo archivo de contraseñas")
		limpiarTodo()
	else:
		guardar("algo")
		archivoActivo=None
		grupo=[]
		buscar()	
		raiz.title("KeyGest 1.0	"+"...........Nuevo archivo de contraseñas")
		limpiarTodo()
	btnNuevoRegistro.config(state="active")
	btnIngresarReg.config(state="active")
	botonBuscar.config(state="active")
	info.set("Nuevo archivo. Introduzca los registros manualmente o importelos desde un archivo CSV")
def abrirArchivo():
	global grupo
	global archivoActivo

	ubicacion=fd.askopenfilename(title="Abrir",initialdir="C:",filetypes=(("Archivos RAG","*.rag"),("Todos los archivos","*.*")))
	nombre="          "+ubicacion[:30]+".........."+ubicacion[ubicacion.rfind("/"):len(ubicacion)]
	if ubicacion!='':	
		abrirArchivo=open(ubicacion,"r")
		try:
			leerArchivo=abrirArchivo.read()
			abrirArchivo.close()
			if archivoActivo!=None:
				guardar("algo")
			try:
				leerArchivo=desencriptar(leerArchivo)
				armarGrupo=eval(leerArchivo)
				grupo=[]
				for i in armarGrupo:
					grupo.append(Contraseña(i[0],i[1],i[2],i[3],i[4],i[5]))
				raiz.title("KeyGest 1.0	"+nombre)
				archivoActivo=ubicacion
				info.set("El archivo fue cargado correctamente")
				limpiarTodo()
				buscar()
				btnNuevoRegistro.config(state="active")
				btnIngresarReg.config(state="active")
				botonBuscar.config(state="active")
			except ValueError:
				info.set("El archivo que intenta abrir no es compatible o está dañado")
		except UnicodeDecodeError:
			info.set("Archivo no permitido")		
def guardar(activo=None):
	global grupo
	global archivoActivo
	#-----------Preparacion de la lista Grupo para su guardado----------
	exportar=[]
	for i in grupo:
		exportar.append(i.mostrar())
	exportCript=encriptar(str(exportar))
	#-------------------------------------------------------------------
	if archivoActivo==None or activo==None: 	#entra en el if si no hay archivo activo o cuando se presiona guardar como
		extenciones=[("Archivos RAG","*.rag")]
		save=fd.asksaveasfilename(filetypes = extenciones, defaultextension = extenciones)	
	else:
		save=archivoActivo						#entra si hay archivo activo y se presiono guardar
	if save!='':								
		abrirSave=open(save, "w", encoding="utf-8")
		try:
			abrirSave.write(str(exportCript))
			abrirSave.close()
			info.set("Archivo Guardado")
			nombre=str(save[:18]+"......"+save[len(save)-25:len(save)])
			raiz.title("KeyGest 1.0	"+"......"+nombre)
			#info.set("Archivo guardado correctamente")
			archivoActivo=save
			btnNuevoRegistro.config(state="active")
			btnIngresarReg.config(state="active")
			botonBuscar.config(state="active")

		except AttributeError:
			info.set("Sin guardar")
	else:
		info.set("Sin guardar")
def guardarRegistro():
	global grupo
	global registroActivo
	global indiceRegAct
	url=varUrl.get()
	email=varEmail.get()
	contraseña=varContraseña.get()
	usuario=varUsuario.get()
	observaciones=varObserv.get()
	yaExiste=None
	for i in range (len(grupo)):	
		if grupo[i].url==url and grupo[i].email==email:
			
			yaExiste=i
			break
	if yaExiste==None:
		if "@" in email:
			if "."in url:	
				grupo.append(Contraseña(url,email,contraseña,usuario,observaciones))
				guardar("algo")
				info.set("Registro ingresado correctamente: Actualmente existen "+str(len(grupo))+" registros en el archivo.")
			else:
				info.set("Error al cargar: Dirección Url no válida...pendiente: quitar color rojo al comenzar a escribir")
				dispUrl.config(bg="#DD7777")			
		else:
			info.set("Error al cargar:  Email no válido... pendiente: quitar color rojo al comenzar a escribir")
			dispMail.config(bg="#DD7777")
	else:
		if grupo[yaExiste].contraseña!=contraseña:
			if mb.askyesno(message="Desea actualizar la contraseña?",title="Advertencia"):
				aHistorial=grupo[yaExiste].contraseña
				grupo[yaExiste]=Contraseña(url,email,contraseña,usuario,observaciones)
				grupo[yaExiste].historial.append(aHistorial)
				info.set("Se ha actualizado la contraseña y se ha guardado la anterior en el historial del registro")
		elif grupo[yaExiste].usuario!=usuario:
			grupo[yaExiste].usuario=usuario
			info.set("El contenido del registro se ha actualizado correctamente")
		else:
			info.set("Ya existe un registro para esa cuenta")
def eliminarRegistro():
	global indiceRegAct
	try:
		grupo[indiceRegAct]
		if mb.askyesno(message="Desea eliminar el registro?",title="Advertencia"):
			grupo.pop(indiceRegAct)
			limpiarTodo()
			buscar()
	except TypeError:
		info.set("Seleccione y cargue el registro que desea eliminar")
def buscar(event=None):
	global grupo
	global listResult
	resultados=[]
	entrada=aBuscar.get()
	if entrada=="":
		info.set("Escriba lo que quiere buscar o escriba * para ver todo")
		varLista.set("Especifique lo que quiere buscar")
	else:
		if entrada=="*":		#si el usuario quere ver todo
			entrada=""			#la cadena vacia devuelve como resultado todos los elementos de la lista
		for i in range (len(grupo)):
			if entrada in grupo[i].url or entrada in grupo[i].email:
				resultados.append([i,grupo[i].url,"/",grupo[i].email])

		cantidadRes=len(resultados)
		if cantidadRes!=0:
			varLista.set("Seleccione un resultado y presione el boton cargar")
			listResult.destroy()
			listResult=OptionMenu(barraBuscar,varLista,*resultados)
			listResult.grid(row=1,column=3)
			listResult.config(width=46)
			if cantidadRes==1:
				info.set("Se obtuvo 1 resultado para su busqueda")
			else:
				info.set("Se obtuvieron "+str(cantidadRes)+" resultados para su busqueda")
		else:
			listResult.destroy()
			varLista.set("No se encontraron resultados")
			listResult=OptionMenu(barraBuscar,varLista,"")
			listResult.grid(row=1,column=3)
			listResult.config(width=46)
			info.set("No hay resultados para la busqueda. Busque por aproximación")
def generarContraseña(nivel):
	def cambiar(nueva):
		global registroActivo
		dispContr2.destroy()
		btnGrabar.destroy()
		btnCancel.destroy()		
		if registroActivo!=None:
			registroActivo.historial.append(str(registroActivo.contraseña))
			registroActivo.contraseña=nueva
		varContraseña.set(nueva)
		info.set("Contraseña actualizada exitosamente")
		
	def cancelar():
		dispContr2.destroy()
		btnGrabar.destroy()
		btnCancel.destroy()
		info.set("Operacion Cancelada")

	caracteres="abcdefghijklmnopqrstuvwxyz+-_/@ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
	randKey=""
	for i in range(nivel):
		a=caracteres[randrange(len(caracteres))]
		randKey=randKey+a
	info.set("Presione Grabar para actualizar la contraseña o Cancelar para conservar la anterior")
	dispContr2=Label(contrFrame,width=21,font=("Calisto MT",13,"bold"),text=randKey)
	dispContr2.grid(row=1,column=1,sticky="W")
	btnGrabar=Button(contrFrame,width=6,text="Grabar",font=("Arial",11),bg="#CCEECC",command=partial(cambiar,randKey))
	btnGrabar.grid(row=1,column=1,sticky="E")
	btnCancel=Button(contrFrame,width=5,text="Cancel",font=("Arial",11),bg="#EECCCC",command=partial(cancelar))
	btnCancel.grid(row=1,column=2)
def mostrarRegistro():
	global indiceRegAct
	global registroActivo
	try:
		indiceRegAct=int(varLista.get().replace(",","    ")[1:5])
		registroActivo=grupo[indiceRegAct]
		varUrl.set(registroActivo.url)
		varEmail.set(registroActivo.email)
		varContraseña.set(registroActivo.contraseña)
		varUsuario.set(registroActivo.usuario)
		btnHisto.config(state="active")
		btnEliminarReg.config(state="active")

	except ValueError:
		varLista.set("SELECCIONE UNA OPCION DE LA LISTA")	
def copiar(que):
	aClipBoard=que.get()
	raiz.clipboard_clear()
	raiz.clipboard_append(aClipBoard)
def pegar(donde):	
	deClipBoard=raiz.clipboard_get()
	donde.set(deClipBoard)
def mostrarContraseña():
	global dispContr
	if dispContr.cget("show")=="*":
		dispContr.config(show="")
		
		verContr.config(image=imgNoVer)
		info.set("Se recomienda mantener la contraseña oculta: usted puede estar siendo vigilado")
	else:
		dispContr.config(show="*")
		verContr.config(image=imgVer)	
		info.set("Asi esta mejor :)")
def historial():
	global registroActivo
	print(registroActivo.historial)
def limpiarTodo():
	global indiceRegAct
	global registroActivo
	varUrl.set("")
	varEmail.set("")
	varContraseña.set("")
	varUsuario.set("")
	varObserv.set("")
	info.set("")
	indiceRegAct=None
	registroActivo=None
	btnHisto.config(state="disabled")
	btnEliminarReg.config(state="disabled")
	varLista.set("Seleccione un elemento de la lista")
def importCsv():
	global grupo
	objetoCsv=fd.askopenfilename(title="Importar CSV",initialdir="C:",filetypes=(("Archivos CSB","*.csv"),("Todos los archivos","*.*")))
	csvLista=[]
	convertContrList=[]
	try:
		with open(objetoCsv,"r") as archivo:
			for linea in archivo:
				csvLista.append(linea.split(","))

		if csvLista[0]==['url', 'email', ' usuario', 'contraseña\n']:
			for i in csvLista:
				url=i[0]
				email=i[1]
				usuario=i[2]
				contraseña=i[3]
				grupo.append(Contraseña(url,email,contraseña[:len(contraseña)-1],usuario))
		else:
			for i in csvLista:
				url=i[0]
				contraseña=i[3]
				if '@' in i[2]:
					email=i[2]
					grupo.append(Contraseña(url,email,contraseña[:len(contraseña)-1],""))
				else:
					usuario=i[2]
					grupo.append(Contraseña(url,"",contraseña[:len(contraseña)-1],usuario))	
		btnNuevoRegistro.config(state="active")
		btnIngresarReg.config(state="active")
		botonBuscar.config(state="active")
		info.set("Archivo CVS importao correctamente. Fueron agregados "+str(len(csvLista))+" registros al archivo")
	except FileNotFoundError:
		pass	
def exportCsv():
	global grupo
	export="url,email, usuario,contraseña\n"
	if mb.askyesno("Advertencia: ","Al exportar en formato CVS cualquiera que abra el archivo CVS podrá ver las contraseñas que contiene.\n Desea exportar de todos modos?"):
		for i in grupo:
			export=export+i.url+','+i.email+','+i.usuario+','+i.contraseña+'\n'
		extenciones=[("Archivos csv","*.csv")]
		saveUbicacion=fd.asksaveasfilename(filetypes = extenciones, defaultextension = extenciones)
		try:
			archSalida=open(saveUbicacion,"w")
			archSalida.write(export)
			archSalida.close()
		except FileNotFoundError and FileNotFoundError:
			pass
def cerrar():
	global grupo
	global archivoActivo
	if archivoActivo!=None:
		if mb.askyesno("Guardar cambios","Desea guardar los cambios efectuados?"):
			guardar("algo")
		limpiarTodo()
		archivoActivo=None
		grupo=[]
		buscar()
		raiz.title("KeyGest 1.0	")
def salir():
	respuesta= mb.askyesno("Cuidado", "¿Quiere salir del programa?")
	if respuesta==True:
		raiz.destroy()	
#--------------------- Atajos de teclado-------------------
def shortcut(event):
	if event.char=="": abrirArchivo()
	elif event.char=="": guardar("algo")
	elif event.char=="": nuevo()
	elif event.char=="": exportCsv()
	elif event.char=="\t": importCsv()
raiz.bind("<Key>", shortcut)

#-------------------- Barra de Menú------------------------

menuArchivo=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Archivo",menu=menuArchivo)
menuArchivo.add_command(label="Nuevo                              Ctrl/n",command=partial(nuevo))
menuArchivo.add_command(label="Abrir                                Ctrl/o",command=abrirArchivo)
menuArchivo.add_command(label="Guardar                           Ctrl/s",command=partial(guardar,"como"))
menuArchivo.add_command(label="Guardar Como",command=partial(guardar))
menuArchivo.add_command(label="Cerrar",command=partial(cerrar))
menuArchivo.add_separator()
menuArchivo.add_command(label="Importar CSV                  Ctrl/i",command=partial(importCsv))
menuArchivo.add_command(label="Exportar CSV                  Ctrl/e",command=partial(exportCsv))
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir",activebackground="#AA3333",command=partial(salir))

menuEdicion=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Edicion",menu=menuEdicion)
menuEdicion.add_command(label="Deshacer")
menuEdicion.add_command(label="Rehacer")
menuEdicion.add_command(label="Copiar Todo")

menuVer=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Ver",menu=menuVer)
menuVer.add_command(label="Ver zócalo informativo")
menuVer.add_command(label="Ver historial de contraseñas")

menuConfiguracion=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Configuración",menu=menuConfiguracion)
nivelContr=Menu(menuConfiguracion,tearoff=0)
menuConfiguracion.add_command(label="Nivel se seguridad")

menuAyuda=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)
menuAyuda.add_command(label="Manual")
menuAyuda.add_separator()
menuAyuda.add_command(label="Acerca de")
#--------------------------------------------------------------
#--------Frame para los botones "copiar"----------------------

imgFondo=PhotoImage(file="llaves.png")
fondo=Label(raiz,image=imgFondo).grid(row=2,column=1,rowspan=5)
botonesFrame=Frame(raiz)
botonesFrame.grid(row=2,column=3,rowspan=4)
#--------------------------------------------------------------
#-----------Label y Entry del campo url------------------------
labUrl=Label(raiz,width=15,text="Url de la Pagina",font=('Arial Black',11))
labUrl.grid(row=2,column=1)
dispUrl=Entry(raiz,width=30,font=(Fuente),textvariable=varUrl)
dispUrl.grid(row=2,column=2,sticky="W")
copiUrl=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varUrl))
copiUrl.grid(row=2,column=2,padx=10,sticky="E")
#---------------------------------------------------------------
#----------Label y Entry del campo Email-------------------------
labMail=Label(raiz,width=15,text="Email registrado",font=('Arial Black',11))
labMail.grid(row=3,column=1)
dispMail=Entry(raiz,width=30,font=(Fuente),textvariable=varEmail)
dispMail.grid(row=3,column=2,sticky="W")
copiMail=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varEmail))
copiMail.grid(row=3,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#----------Label y Entry del campo Usuario ----------------------
labUsu=Label(raiz,width=15,text="Nombre Usuario",font=('Arial Black',11))
labUsu.grid(row=4,column=1)
dispUsu=Entry(raiz,width=30,font=(Fuente),textvariable=varUsuario)
dispUsu.grid(row=4,column=2,sticky="W")
copiUsu=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varUsuario))
copiUsu.grid(row=4,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#----------Label , Entry y botones del campo contraseña ---------
labContr=Label(raiz,width=15,text="Contraseña",font=('Arial Black',9))
labContr.grid(row=5,column=1,sticky="w")
#----------Boton historial  ---------------
btnHisto=Button(raiz,text="Historial",font=('Arial Black',10),bg="#BBBBFF",state="disabled",command=partial(historial))
btnHisto.grid(row=5,column=1,sticky="e")

contrFrame=Frame(raiz)
contrFrame.grid(row=5,column=2)

dispContr=Entry(contrFrame,width=27,font=("Calisto MT",14,"bold" ),textvariable=varContraseña,show="*")
dispContr.grid(row=1,column=1,sticky="W")

imgVer=PhotoImage(file="abrirOjo.PNG")
imgNoVer=PhotoImage(file="cerrarOjo.PNG")
verContr=Button(contrFrame,image=imgVer,command=partial(mostrarContraseña))
verContr.grid(row=1,column=1,sticky="E")

botonRandom=Button(contrFrame,width=5,text="Nueva",font=("Arial",11),bg="#CCCCCC")
botonRandom.grid(row=1,column=2)
botonRandom.config(command=partial(generarContraseña,20))
copiContr=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varContraseña))
copiContr.grid(row=5,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#-------------------- Ingresar y eliminar registro-----------------------
btnNuevoRegistro=Button(raiz,text="Nuevo Registro",font=Fuente,bg="#CCFFCC",state="disabled")
btnNuevoRegistro.grid(row=6,column=1,sticky="e")
btnIngresarReg=Button(raiz,text="Guardar Registro",font=Fuente,bg="#CCFFCC",state="disabled",command=partial(guardarRegistro))
btnIngresarReg.grid(row=6,column=2,sticky="w")
btnEliminarReg=Button(raiz,text="Eliminar Registro",font=Fuente,bg="#FFCCCC",state="disabled",command=partial(eliminarRegistro))
btnEliminarReg.grid(row=6,column=2,sticky="e")
btnLimpiar=Button(raiz,text="Limpiar",font=("Arial Black",10),command=partial(limpiarTodo))
btnLimpiar.grid(row=6,column=3 )

#--------------------barra de busqueda-----------------------
aBuscar=StringVar()
varLista=StringVar(barraBuscar)

botonBuscar=Button(barraBuscar,width=6,text="Buscar",state="disabled",bg="#CCCCCC")
botonBuscar.grid(row=1,column=1,sticky="W")
botonBuscar.config(command=partial(buscar))

entrada=Entry(barraBuscar,width=12,font=("Arial",14),textvariable=aBuscar,bg="#DDDDDD")
entrada.grid(row=1,column=2,sticky="E")
entrada.bind('<Return>', buscar)

listResult=OptionMenu(barraBuscar,varLista,resultados)
listResult.grid(row=1,column=3)
listResult.config(width=46)

botonCargar=Button(barraBuscar,width=7,text="Cargar",bg="#CCCCCC")
botonCargar.grid(row=1, column=4)
botonCargar.config(command=partial(mostrarRegistro))
#-------------------------------------------------------------
#--------- zócalo informativo inferior------------------------
campoInfo=Frame(raiz)
campoInfo.grid(row=8,column=1,padx=10,columnspan=3)
infoLabel0=Label(campoInfo,width=4,font=("Arial",10),text=" Info: ",bg="#999999")
infoLabel0.pack(side="left")

infoLabel=Label(campoInfo,width=67,font=("Arial",10),textvariable=info,justify="left",bg="#999999")
infoLabel.pack(side="right",expand=True)

raiz.mainloop()
