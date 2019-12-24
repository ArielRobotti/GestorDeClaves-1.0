from codecs import*

def encriptar(texto,clave="1234"):
	# aC=clave.encode('utf-8')
	# bC=aC.hex()
	# bC=int(bC,16)

	paso1=texto.encode('utf-8')
	paso2=paso1.hex()
	paso3=int(paso2,16)	

	return paso3

def desencriptar(texto,clave="1234"):
	# aC=clave.encode('utf-8')
	# bC=aC.hex()
	# bC=int(bC,16)

	paso1=hex(int(texto)).replace("0x","")
	paso2=decode(paso1,"hex")
	paso3=paso2.decode('utf-8')

	return paso3







	

