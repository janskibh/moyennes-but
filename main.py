import requests
from bs4 import BeautifulSoup
import json
import getpass

s = requests.session()

exec_request = s.get("https://cas2.uvsq.fr/cas/login?service=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2Fservices%2FdoAuth.php%3Fhref%3Dhttps%253A%252F%252Fbulletins.iut-velizy.uvsq.fr%252F")
exec_request_html = BeautifulSoup(exec_request.text, 'html.parser')
execution = exec_request_html.find('input', {'name':'execution'}).get('value')

data = {
    "username": input("Numéro étudiant : "),
    "password": getpass.getpass("Mot de passe : "),
    "execution": execution,
    "_eventId":"submit",
    "geolocalisation": ""
}

authentification = s.post("https://cas2.uvsq.fr/cas/login?service=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2Fservices%2FdoAuth.php%3Fhref%3Dhttps%253A%252F%252Fbulletins.iut-velizy.uvsq.fr%252F", data = data)
request = s.get("https://bulletins.iut-velizy.uvsq.fr/services/doAuth.php?href=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2F")
request_html = BeautifulSoup(request.text, 'html.parser')
notes_request = s.get("https://bulletins.iut-velizy.uvsq.fr/services/data.php?q=relev%C3%A9Etudiant&semestre=415")
notes = json.loads(notes_request.text)

print("\n")

for ue in notes['relevé']['ues']:
    moyennes = []
    coeffs = []
    coef_total = 0
    moyenne_total = 0
    for r in notes['relevé']['ues'][ue]['ressources']:
        if not notes['relevé']['ues'][ue]['ressources'][r]['moyenne'] == "~":
            moy = float(notes['relevé']['ues'][ue]['ressources'][r]['moyenne'])
            cof = float(notes['relevé']['ues'][ue]['ressources'][r]['coef'])
            moyennes.append(moy*cof)
            coeffs.append(cof)

    for sae in notes['relevé']['ues'][ue]['saes']:
        if not notes['relevé']['ues'][ue]['saes'][sae]['moyenne'] == "~":
            moy = float(notes['relevé']['ues'][ue]['saes'][sae]['moyenne'])
            cof = float(notes['relevé']['ues'][ue]['saes'][sae]['coef'])
            moyennes.append(moy*cof)
            coeffs.append(cof)

    for c in coeffs:
        coef_total += c
        
    for m in moyennes:
        moyenne_total += m

    print(ue + " : " + str(round(moyenne_total/coef_total, 2)))

absences = notes['relevé']['semestre']['absences']['total']
absences_injustifiées = notes['relevé']['semestre']['absences']['injustifie']


print("\nAbsences injustifiées : " + str(absences_injustifiées) + "/" + str(absences))

input("Press ENTER to exit...")
