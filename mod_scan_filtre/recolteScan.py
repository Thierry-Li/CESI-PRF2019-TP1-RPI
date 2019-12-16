from bluepy.btle import Scanner, DefaultDelegate
from datetime import datetime


# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

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

					print(valeurId)
					print(temperature)
					print("1 capteur")

					with open('recolteDonneesScan.txt', 'a') as the_file:
						the_file.write("date et heure : {} / ID : {} / temp : {0:.2f}°C / batterie : {}% \n".format(dt_string, valeurId, temperature, valeurBatterie))
				else :
					print("rien")
