class Contraseña():
	url=""
	email=""
	contraseña=""
	usuario=""
	observaciones=""

	def __init__(self,_URL=None,_Email=None,_Contraseña=None,_usuario=None,_observaciones=None):
		self.url=_URL
		self.email=_Email
		self.contraseña=_Contraseña
		self.usuario=_usuario
		self.observaciones=_observaciones


	def mostrar(self):
		return[self.url,self.email,self.contraseña,self.usuario,self.observaciones]




