class Contraseña():
	url=""
	email=""
	contraseña=""
	usuario=""
	observaciones=""
	historial=[]

	def __init__(self,_URL="",_Email="",_Contraseña="",_usuario="",_observaciones=""):
		self.url=_URL
		self.email=_Email
		self.contraseña=_Contraseña
		self.usuario=_usuario
		self.observaciones=_observaciones
	
		

	def mostrar(self):
		return[self.url,self.email,self.contraseña,self.usuario,self.observaciones,self.historial]



