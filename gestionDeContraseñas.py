'''Este proyecto consiste, por el momento, en una interface 
gráfica para la manipulación y resguardado de contraseñas '''

from tkinter import * 
from functools import * 
from hashlib import *
from claseContr import *
from tkinter import messagebox as mb
from time import *

raiz=Tk()
raiz.geometry("640x300")
raiz.title("Gestor de contraseñas 1.0")
raiz.iconbitmap("llaves.ico")
raiz.resizable(0,0)

resultados=[]
grupo=[]
varUrl=StringVar()
varEmail=StringVar()
varContraseña=StringVar()
varUsuario=StringVar()
varObserv=StringVar()
info=StringVar()

barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)

def guardarContraseña():
	bandera=True
	url=varUrl.get()
	email=varEmail.get()
	contraseña=varContraseña.get()
	usuario=varUsuario.get()
	observaciones=varObserv.get()

	for i in grupo:
		bandera=True
		if i.url==url and i.email==email:
			info.set("Ya existe un registro para esa cuenta")
			bandera=False

	if bandera==True:
		if "@" in email:
			if "."in url:	
				grupo.append(Contraseña(url,email,contraseña,usuario,observaciones))
				info.set("Registro ingresado correctamente: Actualmente existen "+str(len(grupo))+" registros en el archivo.")
			else:
				info.set("Error al cargar: Dirección Url no válida")
				dispUrl.config(bg="red")			
		else:
			info.set("Error al cargar:  Email no válido")
			dispMail.config(bg="red")
def salir():
	respuesta= mb.askyesno("Cuidado", "¿Quiere salir del programa?")
	if respuesta==True:
		raiz.destroy()


def buscar():
	global grupo
	resultados=[]
	entrada=aBuscar.get()		
	for i in range (len(grupo)):
		if entrada in grupo[i].url or entrada in grupo[i].email:
			resultados.append((grupo[i].url,'/',grupo[i].email))
	print("resultados: ",resultados)
	cantidadRes=len(resultados)
	if cantidadRes!=0:
		varLista.set(resultados[0])
		listResult=OptionMenu(barraBuscar,varLista,*resultados).grid(row=1,column=3)
		if cantidadRes==1:
			info.set("Se obtuvo 1 resultado para su busqueda")
		else:
			info.set("Se obtuvieron "+str(cantidadRes)+" resultados para su busqueda")
	else:
		info.set("No hay resultados para la busqueda")

menuArchivo=Menu(barraMenu,tearoff=0,activeborderwidth=4)
barraMenu.add_cascade(label="Archivo",menu=menuArchivo)
menuArchivo.add_command(label="Nuevo")
menuArchivo.add_command(label="Abrir")
menuArchivo.add_command(label="Guardar",command=partial(guardarContraseña))
menuArchivo.add_command(label="Guardar Como")
menuArchivo.add_command(label="Cerrar")
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir",activebackground="Red",command=partial(salir))

menuEdicion=Menu(barraMenu,tearoff=0,activeborderwidth=4)
barraMenu.add_cascade(label="Edicion",menu=menuEdicion)
menuEdicion.add_command(label="Deshacer")
menuEdicion.add_command(label="Rehacer")
menuEdicion.add_command(label="Copiar Todo")

menuBuscar=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Buscar",menu=menuBuscar)
menuBuscar.add_command(label="Buscar registro",command=partial(buscar))

menuHerramientas=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Herramientas",menu=menuHerramientas)
herramConfig=Menu(menuHerramientas,tearoff=0)
menuHerramientas.add_command(label="Configuracion")


menuAyuda=Menu(barraMenu,tearoff=0)
barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)
menuAyuda.add_command(label="Manual")
menuAyuda.add_separator()
menuAyuda.add_command(label="Acerca de")

def nuevaContraseña(url,email,contraseña,usuario="Desconocido",observaciones="Ninguna"):
	pass

def mostrarRegistro(contraseña):
	varUrl.set(contraseña.url)
	varEmail.set(contraseña.email)
	varContraseña.set(contraseña.contraseña)
	varUsuario.set(contraseña.usuario)
	varObserv.set(contraseña.observaciones)

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
		verContr.config(text="ocultar")		
	else:
		dispContr.config(show="*")
		verContr.config(text="ver")	

prueba=Contraseña("youtube.com","changocardenas@gmail.com","rupertoElGoma","gual_disnei")
mostrarRegistro(prueba)

imgFondo=PhotoImage(file="llaves.png")
fondo=Label(raiz,image=imgFondo).grid(row=2,column=1,rowspan=5)


labUrl=Label(raiz,width=15,text="Url de la Pagina",font=("Arial",13))
labUrl.grid(row=2,column=1)
dispUrl=Entry(raiz,width=25,font=("Arial",18),textvariable=varUrl)
dispUrl.grid(row=2,column=2)
copiUrl=Button(raiz,width=5,text="copiar",font=("Arial",14),command=partial(copiar,varUrl))
copiUrl.grid(row=2,column=3,sticky="E",pady=2)

labMail=Label(raiz,width=15,text="Email registrado",font=("Arial",13))
labMail.grid(row=3,column=1)
dispMail=Entry(raiz,width=25,font=("Arial",18),textvariable=varEmail)
dispMail.grid(row=3,column=2)
copiMail=Button(raiz,width=5,text="copiar",font=("Arial",14),command=partial(copiar,varEmail))
copiMail.grid(row=3,column=3,sticky="E",pady=2)

labUsu=Label(raiz,width=15,text="Nombre de Usuario",font=("Arial",13))
labUsu.grid(row=4,column=1)
dispUsu=Entry(raiz,width=25,font=("Arial",18),textvariable=varUsuario)
dispUsu.grid(row=4,column=2)
copiUsu=Button(raiz,width=5,text="copiar",font=("Arial",14),command=partial(copiar,varUsuario))
copiUsu.grid(row=4,column=3,sticky="E",pady=2)

labContr=Label(raiz,width=15,text="Contraseña",font=("Arial",13))
labContr.grid(row=5,column=1)
dispContr=Entry(raiz,width=24,font=("Arial",14),textvariable=varContraseña,show="*")
dispContr.grid(row=5,column=2,sticky="W")
verContr=Button(raiz,width=5,text="ver",font=("Arial Black",10),command=partial(mostrarContraseña))
verContr.grid(row=5,column=2,sticky="E")
copiContr=Button(raiz,width=5,text="copiar",font=("Arial",14),command=partial(copiar,varContraseña))
copiContr.grid(row=5,column=3,sticky="E")

labExtra=Label(raiz,width=15,text="Observaciones",font=("Arial",13))
labExtra.grid(row=6,column=1)
dispExtra=Entry(raiz,width=25,font=("Arial",18),textvariable=varObserv).grid(row=6,column=2)
copiExtra=Button(raiz,width=5,text="pegar",font=("Arial",14),command=partial(pegar,varObserv))
copiExtra.grid(row=6,column=3,sticky="E",pady=2)


aBuscar=StringVar()
barraBuscar=Frame(raiz)
barraBuscar.grid(row=7,column=1,columnspan=2)

entrada=Entry(barraBuscar,width=15,font=(13),textvariable=aBuscar)
entrada.grid(row=1,column=2,sticky="E")

varLista=StringVar(barraBuscar)
varLista.set("					")

listResult=OptionMenu(barraBuscar,varLista,resultados)
listResult.grid(row=1,column=3)

botonBuscar=Button(barraBuscar,width=7,text="Buscar",bg="#CCCCCC")
botonBuscar.grid(row=1,column=1,sticky="W")
botonBuscar.config(command=partial(buscar))

botonRandom=Button(raiz,width=11,text="NuevaClave",font=("Arial Black",10),bg="#AA8888")
botonRandom.grid(row=7,column=3)

campoInfo=Frame(raiz)
campoInfo.grid(row=8,column=1,pady=10,columnspan=3)
infoLabel0=Label(campoInfo,width=4,font=("Arial",10),text=" Info: ",bg="#999999")
infoLabel0.pack(side="left")

infoLabel=Label(campoInfo,width=67,font=("Arial",10),textvariable=info,justify="left",bg="#999999")
infoLabel.pack(side="right",expand=True)	

raiz.mainloop()

