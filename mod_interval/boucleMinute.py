import time
from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate
# Import library pour le script acces mail et accès smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y - %H:%M:%S")


def envoiMail(name, valeurId, temperature, valeurBatterie, isTemperatureKO):
	# creation de l'objet
	msg = MIMEMultipart()

	# On cree une variable 'message' ou on met notre message
	messageKO = "Bonjour,\nà la date et heure {}, le capteur {} avec le numéro d'identification n° {} a une température en dehors du seuil 24 - 30°C.\nLa température du vivarium est actuellement de {0:.2f} °C.\nVeuillez vérifier et règler la température du vivarium en consèquence, merci.\n\nNote à part, le pourcentage de batterie du capteur est de {} %".format(dt_string, name, valeurId, temperature, valeurBatterie)

	messageOK = "Bonjour,\nà la date et heure {}, le capteur {} avec le numéro d'identification n° {} a retrouvé une température comprise dans le seuil 24 - 30°C.\nLa température du vivarium est actuellement de {0:.2f} °C.\n\nNote à part, le pourcentage de batterie du capteur est de {} %".format(dt_string, name, valeurId, temperature, valeurBatterie)


	# On déclare 3 variables avec 3 paramétres différents (l'éxpediteur, le destinataire et le sujet) + une variable de mdp
	password = "F7jKDYPhcv5M2t6"
	msg['From'] = "pythontest3333@gmail.com"
	msg['To'] = "kibidogi@gmail.com"
	msg['Subject'] = dt_string + " Alerte Température vivariums VIVALAND"

	# Ajout dans le corps du message
	# if True
	if(isTemperatureKO):
		msg.attach(MIMEText(messageKO, 'plain'))
	# if False
	else:
		msg.attach(MIMEText(messageOK, 'plain'))

	# Création du serveur
	server = smtplib.SMTP_SSL('smtp.gmail.com: 465')

	# Identification du script avec l'adresse et le mot de passe dans gmail
	server.login(msg['From'], password)


	# Envoi du message via le serveur
	server.sendmail(msg['From'], msg['To'], msg.as_string())

	# Fermeture du serveur
	server.quit()

def scanDevices():
	class ScanDelegate(DefaultDelegate):
		def __init__(self):
			DefaultDelegate.__init__(self)

	scanner = Scanner().withDelegate(ScanDelegate())
	devices = scanner.scan(10.0)

	for dev in devices:
		# getScanData récupère les données adtype, desc et value (qui sont des tuples)
		#creation de la variable dictionnaire pour les adtype et pour les temperatures
		adtype8 = ""
		adtype22 = ""
		dicoTemperature = {}

		for (adtype, value) in dev.getScanData():


			if adtype == 8:
				adtype8 = value
			if adtype == 22:
				adtype22 = value

		if len(adtype22) == 38 and adtype22[4:10] == "113901" and adtype22[32:39] == "000000" :
			if 11000000 < int(adtype22[12:20]) < 12000000:
				# save l'index correspondant au numéro d'identification dans var valeurId
				valeurId = adtype22[12:20]
				# save l'index correspondant à la valeur batterie dans var valeurBatterieHexa
				valeurBatterieHexa = adtype22[20:22]
				# save l'index correspondant à la valeur température dans var valeurtempHexa
				valeurTempHexa = adtype22[24:28]

				# convert hexa to decimal (nomVar_D, base16)
				# On convertit l'hexa de la batterie en decimale
				valeurBatterie = int(valeurBatterieHexa, 16)

				# On convertit l'hexa de la temperature en decimale
				valeurTemp = int(valeurTempHexa, 16)

				#On deplace la décimale vers la gauche de 2
				temperature = valeurTemp * (1/100)

				# print pour voir ce qui est renvoyé
				print(time.strftime('%d/%m/%Y - %H:%M:%S'))
				print(adtype8)
				print(valeurId)
				print("{0:.2f}".format(temperature))
				print(valeurBatterie)


				# vérifie la température avec le seuil :
				# si c'est en dehors du seuil
				if valeurTemp < 2400 or valeurTemp > 3000 :
					# vérifie le capteur est deja dans le dictionnaire dicoTemperature
					if adtype8 not in dicoTemperature :
						# si le capteur n'est pas dedans, il ajoute le capteur et sa temp dedans puis envoi le mail messageKO de danger
						dicoTemperature.update({adtype8: valeurTemp})
						envoiMail(adtype8, valeurId, temperature, valeurBatterie, bool(True))

						# Message qui s'affiche si le mail a été envoyé avec succés
						print ("Enregistrement des températures pour les capteurs. Mail envoyé avec succés a %s" % (msg['To']))

				# si c'est compris dans le seuil
				else :
					# vérifie si capteur existant dans dicoTemperature
					if adtype8 in dicoTemperature :
						# si capteur est déjà existant, supprime ses données du dico et envoie un mail messageOK de rétablissement
						del dicoTemperature[adtype8]
						envoiMail(adtype8, valeurId, temperature, valeurBatterie, bool(False))


			else :
				print("probleme if 11000000 >< 12000000")

		else :
			print("probleme if len(adtype22)")




while True:
	heureActuelle = datetime.now()
	dt_string = now.strftime("%d/%m/%Y - %H:%M:%S")

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
		messageBouclePlante = "Bonjour,\nle programme Capteur a planté\nveuillez le fermer et le relancer manuellement en suivant la notice"
		print(messageBouclePlante)


		# On déclare 3 variables avec 3 paramétres différents (l'éxpediteur, le destinataire et le sujet) + une variable de mdp
		password = "F7jKDYPhcv5M2t6"
		msg['From'] = "pythontest3333@gmail.com"
		msg['To'] = "kibidogi@gmail.com"
		msg['Subject'] = dt_string + "Alerte Programme Capteur a planté"

		# Ajout dans le corps du message
		msg.attach(MIMEText(messageBouclePlante, 'plain'))

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

