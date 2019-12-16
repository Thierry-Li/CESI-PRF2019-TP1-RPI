
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



# test temperature en local
value = "ffcb1139012311162856600407981636000000"
valeurTemp = 21
adtype = 22

if adtype == 22:
	if len(value) == 38 and value[4:10] == "113901" and value[32:39] == "000000" :
		if 11000000 < int(value[12:20]) < 12000000:
			valeurId = value[12:20]
			valeurBatterieHexa = value[20:22]
			valeurTempHexa = value[24:28]

			valeurBatterie = int(valeurBatterieHexa, 16)
			valeurTemp = int(valeurTempHexa, 16)
			temperature = valeurTemp * (1/100)

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
				print(valeurId)
				print("{0:.2f}".format(temperature))
				print("pas d'envoie de mail")

		else :
			print("scanné mais pas trouvé les capteurs que l'on cherche")



