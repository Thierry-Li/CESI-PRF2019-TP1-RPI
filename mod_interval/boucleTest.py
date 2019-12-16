import time
from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate
# Import library pour le script acces mail et accès smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")



def scanDevices():
	class ScanDelegate(DefaultDelegate):
		def __init__(self):
			DefaultDelegate.__init__(self)

	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(10.0)

	for dev in devices:
		for (adtype, desc, value) in dev.getScanData():
			if adtype == 22:
				if len(value) == 38 and value[4:10] == "113901" and value[32:39] == "000000" :
					if 11000000 < int(value[12:20]) < 12000000:
						# save l'index correspondant au numéro d'identification dans var valeurId
						valeurId = value[12:20]
						# save l'index correspondant à la valeur batterie dans var valeurBatterieHexa
						valeurBatterieHexa = value[20:22]
						# save l'index correspondant à la valeur température dans var valeurtempHexa
						valeurTempHexa = value[24:28]

						# convert hexa to decimal (nomVar_D, base16)
						# On convertit l'hexa de la batterie en decimale
						valeurBatterie = int(valeurBatterieHexa, 16)

						# On convertit l'hexa de la temperature en decimale
						valeurTemp = int(valeurTempHexa, 16)

						#On deplace la décimale vers la gauche de 2
						temperature = valeurTemp * (1/100)
						print(time.strftime('%H:%M:%S'))
						print(valeurId)
						print("{0:.2f}".format(temperature))
						print(valeurBatterie)
					else :
						print("probleme")




while True:
	heureActuelle = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	try:
		if ((heureActuelle.second % 2) == 0):
			print("try")
			time.sleep(20)
			scanDevices()

	except:
		print("except")
		break
		# creation de l'objet
		msg = MIMEMultipart()

		# On cree une variable 'message' ou on met notre message
		message = "Bonjour,\nle programme Capteur a planté\nveuillez le fermer et le relancer manuellement en suivant la notice"
		print(message)


		# On déclare 3 variables avec 3 paramétres différents (l'éxpediteur, le destinataire et le sujet) + une variable de mdp
		password = "F7jKDYPhcv5M2t6"
		msg['From'] = "pythontest3333@gmail.com"
		msg['To'] = "kibidogi@gmail.com"
		msg['Subject'] = dt_string + "Alerte Programme Capteur a planté"

		# Ajout dans le corps du message
		msg.attach(MIMEText(message, 'plain'))

		# Création du serveur
		server = smtplib.SMTP_SSL('smtp.gmail.com: 465')

		# Identification du script avec l'adresse et le mot de passe dans gmail
		server.login(msg['From'], password)


		# Envoi du message via le serveur
		server.sendmail(msg['From'], msg['To'], msg.as_string())

		# Fermeture du serveur
		server.quit()

		# Message qui s'affiche si le mail a été envoyé avec succés
		print ("Mail envoyé avec succés a %s" % (msg['To']))
		break
	finally:
		if ((heureActuelle.second % 2) == 0):
			print("finally")
			time.sleep(20)
			scanDevices()


	''' if ((heureActuelle.second % 10) == 0):
		stockData() '''
