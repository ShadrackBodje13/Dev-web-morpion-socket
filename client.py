#Le fichier à run pour lancer le projet

import socket
import threading
import sys

#pour l'utilisation de socket on a besoin de port et adresse reseau server
host = '127.0.0.1'
port = 5001

class ThreadReception(threading.Thread):
    	# """objet thread gérant la réception des messages"""
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn # réf. du socket de connexion
	def run(self):
		while 1:
			message_recu = self.connexion.recv(1024).decode("Utf8")
			print("*" + message_recu + "*")
			if not message_recu or message_recu.upper() =="FIN":
				break
		# Le thread <réception> se termine ici.
		# On force la fermeture du thread <émission> :
		th_E._stop()
		print("Client arrêté. Connexion interrompue.")
		self.connexion.close()

class ThreadEmission(threading.Thread):
	"""objet thread gérant l'émission des messages"""
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn # réf. du socket de connexion

	def run(self):
		while 1:
			try:
				message_emis = int(input( " Taper un nombre entre 0 et 8 "))
				if not(0 <= message_emis <= 8):
					raise ValueError()
			except ValueError:
					print("Tapez un ENTIER entre 0 et 8")
			else:
				self.connexion.send(str(message_emis).encode("Utf8"))

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	connexion.connect((host, port))
except socket.error:
	print("La connexion a échoué.")
	sys.exit()
print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()