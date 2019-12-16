# ALGORITHME MAIL RETABLISSEMENT, j'espére que vous pourrez me donner un coup de main :), cdt Yahya
# les grands bouts de codes sont minimisés, vous avez juste a cliquer sur le numero de la ligne pour afficher tout le code
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boucleMinute
from boucleMinute import *
import smtplib
temperature = 24
valeurId = 1112121

# l'algo principale est exécuté, il fait son scan puis vérifie
if valeurTemp < 2400 or valeurTemp > 3000 :
	msg = MIMEMultipart()
	message = "Bonjour,\nà la date et heure {}, le vivarium n°{} du magasin {} a détecté un problème.\nLe capteur avec le numéro d'identification n° {} a une température en dehors du seuil 24 - 30°C.\nLa température du vivarium est actuellement de {} °C.\nVeuillez vérifier et règler la température du vivarium en consèquence, merci.\n\nNote à part, le pourcentage de batterie du capteur est de {} %".format(dt_string, vivarium, animalerie, valeurId, temperature, valeurBatterie)
	password = "F7jKDYPhcv5M2t6"
	msg['From'] = "pythontest3333@gmail.com"
	msg['To'] = "kibidogi@gmail.com"
	msg['Subject'] = dt_string + " Alerte Température vivariums VIVALAND"
	msg.attach(MIMEText(message, 'plain'))
	server = smtplib.SMTP_SSL('smtp.gmail.com: 465')
	server.login(msg['From'], password)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()
	print ("Mail envoyé avec succés a %s" % (msg['To']))
	temp = valeurTemp # ON ENREGISTR DANS UNE VARIABLE 'temp' LA TEMPERATURE DEFAILLANTE POUR LA COMPARER PLUS BAS

# Si les temps respectent le seul alors pas d'envoi de mail
else : # il affiche juste les données qu'il reçoit
	print(time.strftime('%H:%M:%S'))
	print(valeurId)
	print("{0:.2f}".format(temperature))
	print("pas d'envoie de mail")


	scanDevices() # il continue avec son prochain scan
		if temp < 2400 or temp > 3000 : # il vérifie si la temperature respecte le seuil, si respecte pas il affiche un message sinon
			print("une alerte a déjà été envoyé")

		elif temp >= 2400 and temp <= 3000: #si la temperature revient normal donc entre 24 - 30°C alors t'envoi un mail de rétablissement
			msg = MIMEMultipart()
			message = "Bonjour, le {}, le vivarium n°{} du magasin {} a détecté que la température est revenu a la normalité. Le capteur avec le numéro d'identification n°{} a une température qui est compris entre 24 - 30°C. La température du vivarium est actuellement de {} °C".format(dt_string, vivarium, animalerie, valeurId, temp)
			password = "F7jKDYPhcv5M2t6"
			msg['From'] = "pythontest3333@gmail.com"
			msg['To'] = "yahyamazouarenna@gmail.com"
			msg['Subject'] = dt_string + " Rétablissement de la température"

			msg.attach(MIMEText(message, 'plain'))
			server = smtplib.SMTP_SSL('smtp.gmail.com: 465')
			server.login(msg['From'], password)
			server.sendmail(msg['From'], msg['To'], msg.as_string())
			server.quit()
			print ("Mail de rétablissement envoyé avec succés a %s" % (msg['To']))
		else:
			break
