'''
x = int("60", 16)
print(x)
'''

valeurGlobale = "11162856600407981636000000"

valeurId = valeurGlobale[0:8]
valeurBatterie = valeurGlobale[8:10]
valeurTemp = valeurGlobale[12:16]

#check si les valeurs d'index retournent batterie et température
print(valeurId)
print(valeurBatterie)
print(valeurTemp)


print(f"Le numéro d'identification du capteur est : {valeurId}")


#convert hexa to decimal (nomVar_D, base16)
#On convertit l'hexa de la batterie en decimale
valeurBatterie_D = int(valeurBatterie, 16)

#On convertit l'hexa de la batterie en decimale
print(f"Le niveau de la batterie est de : {valeurBatterie_D} %")

#On convertit l'hexa de la temperature en decimale
valeurTemp_D = int(valeurTemp, 16)

#On deplace la décimale vers la gauche de 2
temperature = valeurTemp_D * (1/100)

print(f"La température du capteur est de : {temperature} °C")
