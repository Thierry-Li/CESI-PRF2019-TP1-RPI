# Importation des libraries necessaires
# Import library BLUEPY (pour le scan Bluetooth)
from bluepy.btle import Scanner, DefaultDelegate
# Import library pour le planificateur
import schedule
import time
from datetime import datetime

# Import library pour le script acces mail et accès smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# Import date et heure actuelle
from datetime import datetime


# variable de test pour un numéro vivarium et faux magasin de test en local sans RASPBIAN
vivarium = 3
animalerie = "Vivaland_Bordeaux_Merignac"
# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

'''
# test temperature en local
value = "ffcb1139012311162856600407981636000000"
valeurTemp = 21
adtype = 22
'''

def scanCapteursMail():

	# Class provenant de la library Scanner et DefaultDelegate
	class ScanDelegate(DefaultDelegate):

		def __init__(self):
			DefaultDelegate.__init__(self)

	scanner = Scanner().withDelegate(ScanDelegate())
	# scan d'une durée de 10 secondes
	devices = scanner.scan(10.0)
	# scanner.scan() renvoit les données add Mac/ add Type et le RSSI dans la variable devices
	# dev.addr = adr MAC / dev.addrType = Random ou public / dev.rssi = force signal BLE


	# boucle for qui va parcourir dans les données de la variable devices
	for dev in devices:
	# getScanData récupère les données adtype, desc et value (qui sont des tuples)
		for (adtype, desc, value) in dev.getScanData():

			# boucle condition qui cible les critères de comparaison avec les infos dev que l'on reçoit dans devices
			# vérifie que la value numéro d'identification est comprise entre 11000000 et 12000000
			#if type == 2 and len(value) == 38 and value[4:10] == "113901" and value[32:39] == "000000" and 11000000 < int(value[12:20]) < 12000000 :
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
						liste_data.append((valeurId, temperature, valeurBatterie))
						# vérifie si valeurTemp est comprise entre 24°C et 30°C (2400 et 3000)
						# return les variables en tuples
						yield (valeurId, temperature, valeurBatterie)

						if valeurTemp < 2400 or valeurTemp > 3000 :
							# creation de l'objet
							msg = MIMEMultipart()

							# On cree une variable 'message' ou on met notre message
							message = "Bonjour,\nà la date et heure {}, le vivarium n°{} du magasin {} a détecté un problème.\nLe capteur avec le numéro d'identification n° {} a une température en dehors du seuil 24 - 30°C.\nLa température du vivarium est actuellement de {} °C.\nVeuillez vérifier et règler la température du vivarium en consèquence, merci.\n\nNote à part, le pourcentage de batterie du capteur est de {} %".format(dt_string, vivarium, animalerie, valeurId, temperature, valeurBatterie)
							print(message)


							# On déclare 3 variables avec 3 paramétres différents (l'éxpediteur, le destinataire et le sujet) + une variable de mdp
							password = "F7jKDYPhcv5M2t6"
							msg['From'] = "pythontest3333@gmail.com"
							msg['To'] = "kibidogi@gmail.com"
							msg['Subject'] = dt_string + " Alerte Température vivariums VIVALAND"

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
						else :
							print(time.strftime('%H:%M:%S'))
							print(valeurId)
							print("{0:.2f}".format(temperature))
							print("pas d'envoie de mail")


					else :
						print("scanné mais pas trouvé les capteurs que l'on cherche")





def scanRecolteDonnees():
	(valeurId, temperature, valeurBatterie) = scanCapteursMail()

	print(valeurId)
	print("1 entrée dans le log\n")
	with open('intervalScan.txt', 'a', encoding = "utf-8") as the_file:
		the_file.write("date et heure : {} / ID : {} / temp : {}°C / batterie : {}% \n".format(time.strftime('%d/%m/%Y %H:%M:%S'), valeurId, temperature, valeurBatterie))


schedule.every(2).seconds.do(scanCapteursMail)
schedule.every(10).seconds.do(scanRecolteDonnees)


while True:
	schedule.run_pending()
	time.sleep(1)

