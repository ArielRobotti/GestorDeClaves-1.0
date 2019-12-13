'''Este proyecto consiste, por el momento, en una interface 
gráfica para la manipulación y resguardado de contraseñas '''

from tkinter import * 
from functools import * 
from hashlib import *
from claseContr import *
from tkinter import messagebox as mb
from time import *

raiz=Tk()
raiz.geometry("610x300")
raiz.title("Gestor de contraseñas 1.0")
raiz.iconbitmap("llaves.ico")
#raiz.resizable(0,0)

barraBuscar=Frame(raiz)
barraBuscar.grid(row=7,column=1,columnspan=3,padx=2,pady=6)

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
	global grupo
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
				info.set("Error al cargar: Dirección Url no válida...pendiente: quitar color rojo al comenzar a escribir")
				dispUrl.config(bg="red")			
		else:
			info.set("Error al cargar:  Email no válido... pendiente: quitar color rojo al comenzar a escribir")
			dispMail.config(bg="red")
def salir():
	respuesta= mb.askyesno("Cuidado", "¿Quiere salir del programa?")
	if respuesta==True:
		raiz.destroy()

def buscar():
	global grupo
	global listResult
	resultados=[]
	entrada=aBuscar.get()
	if entrada=="":
		info.set("Escriba lo que quiere buscar o escriba * para ver todo")
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

def mostrarRegistro():

	indice=int(varLista.get().replace(",","    ")[1:5])
	contraseñaSel=grupo[indice]

	varUrl.set(contraseñaSel.url)
	varEmail.set(contraseñaSel.email)
	varContraseña.set(contraseñaSel.contraseña)
	varUsuario.set(contraseñaSel.usuario)
	varObserv.set(contraseñaSel.observaciones)

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
		info.set("Se recomienda mantener la contraseña oculta: usted puede estar siendo vigilado")
	else:
		dispContr.config(show="*")
		verContr.config(text="mostrar")	
		info.set("Asi esta mejor :)")	

for i in ("el","siguiente","texto","tiene","la","finalidad","de","generar","registros","para","probar","el","funcionamiento","de","la","aplicacio","La",
			"revolución", "de",  "Data", "no" ,"solo" ,"se", "refiere", "al" ,"exponencial", "crecimiento", "del", "crecimiento", 
			"de", "los", "datos", "también", "recae", "en", "el", "mejoramiento", "de" ,"los", "métodos", "estadísticos", "y", "computacionales",
			"La", "capacidad" ,"de", "cómputo", "se" ,"dobla", "cada", "18", "meses", "según", "la" ,"Ley", "de" ,"Moore", "pero" ,"eso", "es", "nada", "a", 
			"comparación", "de", "un", "algoritmo", "con", "una", "serie" ,"de", "reglas" ,"que", "puede", "ser", "usado", "para", "resolver" ,"un", 
			"problema", "miles" ,"de" ,"veces", "más", "rápido" ,"que" ,"un", "método", "computacional", "convencional", "Shaw" ,"2014", 
			"He" ,"aquí" ,"la" ,"importancia", "en", "el", "mundo" ,"académico","y","para","rellenar","un","poco","mas","acá","agrego","otro","poco","de",
			"texto","a","ver","si","el","cargador","de","contraseñas","funciona","bien","con","tres","digitos"):
	grupo.append(Contraseña(i+".com",i[2:]+i[:2]+"@gmail.com","rupertoElGoma","gual_disnei","todo bien"))

imgFondo=PhotoImage(file="llaves.png")
fondo=Label(raiz,image=imgFondo).grid(row=2,column=1,rowspan=5)

labUrl=Label(raiz,width=15,text="Url de la Pagina",font=("Arial",13))
labUrl.grid(row=2,column=1)
dispUrl=Entry(raiz,width=30,font=("Arial",15),textvariable=varUrl)
dispUrl.grid(row=2,column=2,sticky="W")
copiUrl=Button(raiz,width=5,text="copiar",font=("Arial",13),command=partial(copiar,varUrl))
copiUrl.grid(row=2,column=3,padx=10,sticky="E")

labMail=Label(raiz,width=15,text="Email registrado",font=("Arial",13))
labMail.grid(row=3,column=1)
dispMail=Entry(raiz,width=30,font=("Arial",15),textvariable=varEmail)
dispMail.grid(row=3,column=2,sticky="W")
copiMail=Button(raiz,width=5,text="copiar",font=("Arial",13),command=partial(copiar,varEmail))
copiMail.grid(row=3,column=3,padx=10,sticky="E")

labUsu=Label(raiz,width=15,text="Nombre Usuario",font=("Arial",13))
labUsu.grid(row=4,column=1)
dispUsu=Entry(raiz,width=30,font=("Arial",15),textvariable=varUsuario)
dispUsu.grid(row=4,column=2,sticky="W")
copiUsu=Button(raiz,width=5,text="copiar",font=("Arial",13),command=partial(copiar,varUsuario))
copiUsu.grid(row=4,column=3,padx=10,sticky="E")

labContr=Label(raiz,width=15,text="Contraseña",font=("Arial",13))
labContr.grid(row=5,column=1)
dispContr=Entry(raiz,width=25,font=("Arial",14),textvariable=varContraseña,show="*")
dispContr.grid(row=5,column=2,sticky="W")
verContr=Button(raiz,width=6,text="mostrar",font=("Arial Black",10),command=partial(mostrarContraseña))
verContr.grid(row=5,column=2,sticky="E")
copiContr=Button(raiz,width=5,text="copiar",font=("Arial",13),command=partial(copiar,varContraseña))
copiContr.grid(row=5,column=3,padx=10,sticky="E")

labExtra=Label(raiz,width=15,text="Observaciones",font=("Arial",13))
labExtra.grid(row=6,column=1)
dispExtra=Entry(raiz,width=30,font=("Arial",14),textvariable=varObserv)
dispExtra.grid(row=6,column=2,sticky="W")
copiExtra=Button(raiz,width=5,text="pegar",font=("Arial",13),command=partial(pegar,varObserv))
copiExtra.grid(row=6,column=3,padx=10,sticky="E")

#--------------------barra de busqueda-----------------------
aBuscar=StringVar()
varLista=StringVar(barraBuscar)

botonBuscar=Button(barraBuscar,width=7,text="Buscar",bg="#CCCCCC")
botonBuscar.grid(row=1,column=1,sticky="W")
botonBuscar.config(command=partial(buscar))

entrada=Entry(barraBuscar,width=18,font=(13),textvariable=aBuscar,bg="#DDDDDD")
entrada.grid(row=1,column=2,sticky="E")

listResult=OptionMenu(barraBuscar,varLista,resultados)
listResult.grid(row=1,column=3)
listResult.config(width=42)

botonCargar=Button(barraBuscar,width=7,text="Cargar",bg="#CCCCCC")
botonCargar.grid(row=1, column=4)
botonCargar.config(command=partial(mostrarRegistro))

#-------------------------------------------------------------

campoInfo=Frame(raiz)
campoInfo.grid(row=8,column=1,padx=10,columnspan=3)
infoLabel0=Label(campoInfo,width=4,font=("Arial",10),text=" Info: ",bg="#999999")
infoLabel0.pack(side="left")

infoLabel=Label(campoInfo,width=67,font=("Arial",10),textvariable=info,justify="left",bg="#999999")
infoLabel.pack(side="right",expand=True)

# botonRandom=Button(raiz,width=11,text="NuevaClave",font=("Arial Black",10),bg="#AA8888")
# botonRandom.grid(row=7,column=3)

raiz.mainloop()
