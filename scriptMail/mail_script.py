# Importation des libraries necessaires

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# creation de l'objet
msg = MIMEMultipart()

# On cree une variable 'message' ou on met notre message
message = "Bonjour, le vivarium n°X, id (xxxxxx) a une température comprise entre 24 - 30°C"

# On déclare 3 variables avec 3 paramétres différents (l'éxpediteur, le destinataire et le sujet) + une variable de mdp
password = "*************"
msg['From'] = "pythontest****@gmail.com"
msg['To'] = "name***@gmail.com"
msg['Subject'] = "Temperature"

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
