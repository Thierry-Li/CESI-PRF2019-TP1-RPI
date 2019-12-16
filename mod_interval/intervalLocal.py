
import schedule
import time
from datetime import datetime


# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# test temperature en local
value = "ffcb1139012311162856600407981636000000"
valeurTemp = 21
adtype = 22


def scanCapteursMail():

	if adtype == 22:
		if len(value) == 38 and value[4:10] == "113901" and value[32:39] == "000000" :
			if 11000000 < int(value[12:20]) < 12000000:

				valeurId = value[12:20]
				valeurBatterieHexa = value[20:22]
				valeurTempHexa = value[24:28]

				valeurBatterie = int(valeurBatterieHexa, 16)
				valeurTemp = int(valeurTempHexa, 16)
				temperature = valeurTemp * (1/100)


				print(time.strftime('%H:%M:%S'))
				print(valeurId)
				print(temperature)
				print(valeurBatterie)
				print("1 capteur\n")
				return valeurId, temperature, valeurBatterie
			else :
				print("aucun capteur")





def scanRecolteDonnees():
	valeurId, temperature, valeurBatterie = scanCapteursMail()

	print(valeurId)
	print("1 entrée dans le log\n")

	with open('intervalLocal.txt', 'a', encoding = "utf-8") as the_file:
		the_file.write("date et heure : {} / ID : {} / temp : {}°C / batterie : {}% \n".format(time.strftime('%d/%m/%Y %H:%M:%S'), valeurId, temperature, valeurBatterie))


schedule.every(2).seconds.do(scanCapteursMail)
schedule.every(10).seconds.do(scanRecolteDonnees)


while True:
	schedule.run_pending()
	time.sleep(1)

