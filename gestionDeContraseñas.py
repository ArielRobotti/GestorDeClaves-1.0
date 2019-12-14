'''Este proyecto consiste, por el momento, en una interface 
gráfica para la manipulación y resguardado de contraseñas '''

from tkinter import * 
from functools import * 
from claseContr import *

raiz=Tk()
raiz.geometry("600x290")
raiz.title("Gestor de contraseñas 1.0")
raiz.iconbitmap("llaves.ico")
raiz.resizable(0,0)

Fuente=("Arial",14)

barraBuscar=Frame(raiz)
barraBuscar.grid(row=7,column=1,columnspan=4,padx=2,pady=6)

resultados=[]
grupo=[]
keygen=0

varUrl=StringVar()
varEmail=StringVar()
varContraseña=StringVar()
varUsuario=StringVar()
varObserv=StringVar()
info=StringVar()

barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)

def guardarRegistro( ):
	global grupo
	yaExiste=""
	url=varUrl.get()
	email=varEmail.get()
	contraseña=varContraseña.get()
	usuario=varUsuario.get()
	observaciones=varObserv.get()

	for i in grupo:
		yaExiste=False
		if i.url==url and i.email==email:
			info.set("Ya existe un registro para esa cuenta")
			yaExiste=True

	if yaExiste==False:
		if "@" in email:
			if "."in url:	
				grupo.append(Contraseña(url,email,contraseña,usuario,observaciones))
				info.set("Registro ingresado correctamente: Actualmente existen "+str(len(grupo))+" registros en el archivo.")
			else:
				info.set("Error al cargar: Dirección Url no válida...pendiente: quitar color rojo al comenzar a escribir")
				dispUrl.config(bg="red")			
		else:
			info.set("Error al cargar:  Email no válido... pendiente: quitar color rojo al comenzar a escribir")
			dispMail.config(bg="red")
def buscar():
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
			listResult.config(width=42)
			if cantidadRes==1:
				info.set("Se obtuvo 1 resultado para su busqueda")
			else:
				info.set("Se obtuvieron "+str(cantidadRes)+" resultados para su busqueda")
		else:
			listResult.destroy()
			varLista.set("No se encontraron resultados")
			listResult=OptionMenu(barraBuscar,varLista,"")
			listResult.grid(row=1,column=3)
			listResult.config(width=42)
			info.set("No hay resultados para la busqueda. Busque por aproximación")
def generarContraseña(nivel):
	def cambiar(nueva):
		dispContr2.destroy()
		btnGrabar.destroy()
		btnCancel.destroy()
		varContraseña.set(nueva)
		info.set("Contraseña actualizada exitosamente")
	def cancelar():
		dispContr2.destroy()
		btnGrabar.destroy()
		btnCancel.destroy()
		info.set("Operacion Cancelada")

	caracteres="abcdefghijklmnñopqrstuvwxyz+-_/@ABCDEFGHIJKLMNÑOPQRSTUVWXYZ123456789"
	devolver=""
	for i in range(nivel):
		a=caracteres[randrange(len(caracteres))]
		devolver=devolver+a
	info.set("Presione Grabar para actualizar la contraseña o Cancelar para conservar la anterior")
	dispContr2=Label(contrFrame,width=21,font=("Calisto MT",13,"bold"),text=devolver)
	dispContr2.grid(row=1,column=1,sticky="W")
	btnGrabar=Button(contrFrame,width=6,text="Grabar",font=("Arial",11),bg="#CCEECC",command=partial(cambiar,devolver))
	btnGrabar.grid(row=1,column=1,sticky="E")
	btnCancel=Button(contrFrame,width=5,text="Cancel",font=("Arial",11),bg="#EECCCC",command=partial(cancelar))
	btnCancel.grid(row=1,column=2)
def mostrarRegistro():
	try:
		indice=int(varLista.get().replace(",","    ")[1:5])
		contraseñaSel=grupo[indice]
		varUrl.set(contraseñaSel.url)
		varEmail.set(contraseñaSel.email)
		varContraseña.set(contraseñaSel.contraseña)
		varUsuario.set(contraseñaSel.usuario)
		varObserv.set(contraseñaSel.observaciones)
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
def salir():
	respuesta= mb.askyesno("Cuidado", "¿Quiere salir del programa?")
	if respuesta==True:
		raiz.destroy()

	
#-------------------- Barra de Menú------------------------

menuArchivo=Menu(barraMenu,tearoff=0,activeborderwidth=4)
barraMenu.add_cascade(label="Archivo",menu=menuArchivo)
menuArchivo.add_command(label="Nuevo")
menuArchivo.add_command(label="Abrir")
menuArchivo.add_command(label="Guardar",command=partial(guardarRegistro))
menuArchivo.add_command(label="Guardar Como")
menuArchivo.add_command(label="Cerrar")
menuArchivo.add_separator()
menuArchivo.add_command(label="Importar CSV")
menuArchivo.add_command(label="Exportar CSV")
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir",activebackground="#AA3333",command=partial(salir))

menuEdicion=Menu(barraMenu,tearoff=0,activeborderwidth=4)
barraMenu.add_cascade(label="Edicion",menu=menuEdicion)
menuEdicion.add_command(label="Deshacer")
menuEdicion.add_command(label="Rehacer")
menuEdicion.add_command(label="Copiar Todo")

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
botonesFrame.grid(row=2,column=3,rowspan=5)
#--------------------------------------------------------------
#-----------Label y Entry del campo url------------------------
labUrl=Label(raiz,width=15,text="Url de la Pagina",font=(Fuente))
labUrl.grid(row=2,column=1)
dispUrl=Entry(raiz,width=30,font=(Fuente),textvariable=varUrl)
dispUrl.grid(row=2,column=2,sticky="W")
copiUrl=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varUrl))
copiUrl.grid(row=2,column=2,padx=10,sticky="E")
#---------------------------------------------------------------
#----------Label y Entry del campo Email-------------------------
labMail=Label(raiz,width=15,text="Email registrado",font=(Fuente))
labMail.grid(row=3,column=1)
dispMail=Entry(raiz,width=30,font=(Fuente),textvariable=varEmail)
dispMail.grid(row=3,column=2,sticky="W")
copiMail=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varEmail))
copiMail.grid(row=3,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#----------Label y Entry del campo Usuario ----------------------
labUsu=Label(raiz,width=15,text="Nombre Usuario",font=(Fuente))
labUsu.grid(row=4,column=1)
dispUsu=Entry(raiz,width=30,font=(Fuente),textvariable=varUsuario)
dispUsu.grid(row=4,column=2,sticky="W")
copiUsu=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varUsuario))
copiUsu.grid(row=4,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#----------Label , Entry y botones del campo contraseña ---------
labContr=Label(raiz,width=15,text="Contraseña",font=(Fuente))
labContr.grid(row=5,column=1)
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
botonRandom.config(command=partial(generarContraseña,18))
copiContr=Button(botonesFrame,width=5,text="copiar",font=(Fuente),command=partial(copiar,varContraseña))
copiContr.grid(row=5,column=2,padx=10,sticky="E")
#----------------------------------------------------------------
#----------Label y Entry del campo Observaciones  ---------------
labExtra=Label(raiz,width=15,text="Observaciones",font=(Fuente))
labExtra.grid(row=6,column=1)
dispExtra=Entry(raiz,width=30,font=(Fuente),textvariable=varObserv)
dispExtra.grid(row=6,column=2,sticky="W")
copiExtra=Button(botonesFrame,width=5,text="pegar",font=(Fuente),command=partial(pegar,varObserv))
copiExtra.grid(row=6,column=2,padx=10,sticky="E")
#--------------------barra de busqueda-----------------------
aBuscar=StringVar()
varLista=StringVar(barraBuscar)

botonBuscar=Button(barraBuscar,width=6,text="Buscar",bg="#CCCCCC")
botonBuscar.grid(row=1,column=1,sticky="W")
botonBuscar.config(command=partial(buscar))

entrada=Entry(barraBuscar,width=15,font=("Arial",14),textvariable=aBuscar,bg="#DDDDDD")
entrada.grid(row=1,column=2,sticky="E")

listResult=OptionMenu(barraBuscar,varLista,resultados)
listResult.grid(row=1,column=3)
listResult.config(width=42)

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
#-------------------------------------------------------------
for i in ("el","siguiente","texto","tiene","la","finalidad","de","generar","registros","para","probar","el","funcionamiento","de","la","aplicacio","La",
			"revolución", "de",  "Data", "no" ,"solo" ,"se", "refiere", "al" ,"exponencial", "crecimiento", "del", "crecimiento", 
			"de", "los", "datos", "también", "recae", "en", "el", "mejoramiento", "de" ,"los", "métodos", "estadísticos", "y", "computacionales",
			"La", "capacidad" ,"de", "cómputo", "se" ,"dobla", "cada", "18", "meses", "según", "la" ,"Ley", "de" ,"Moore", "pero" ,"eso", "es", "nada", "a", 
			"comparación", "de", "un", "algoritmo", "con", "una", "serie" ,"de", "reglas" ,"que", "puede", "ser", "usado", "para", "resolver" ,"un", 
			"problema", "miles" ,"de" ,"veces", "más", "rápido" ,"que" ,"un", "método", "computacional", "convencional", "Shaw" ,"2014", 
			"He" ,"aquí" ,"la" ,"importancia", "en", "el", "mundo" ,"académico","y","para","rellenar","un","poco","mas","acá","agrego","otro","poco","de",
			"texto","a","ver","si","el","cargador","de","contraseñas","funciona","bien","con","tres","digitos"):
	grupo.append(Contraseña(i+".com",i[::-1]+"@gmail.com","weruhwerijds","gual_disnei","todo bien"))


raiz.mainloop()


