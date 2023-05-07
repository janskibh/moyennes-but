import requests
from bs4 import BeautifulSoup
import json
import getpass
import base64

s = requests.session()

exec_request = s.get("https://cas2.uvsq.fr/cas/login?service=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2Fservices%2FdoAuth.php%3Fhref%3Dhttps%253A%252F%252Fbulletins.iut-velizy.uvsq.fr%252F")
exec_request_html = BeautifulSoup(exec_request.text, 'html.parser')
execution = exec_request_html.find('input', {'name':'execution'}).get('value')

data = {
    "username": input("Identifiant : "),
    "password": getpass.getpass("Mot de passe : "),
    "execution": execution,
    "_eventId":"submit",
    "geolocalisation": ""
}

authentification = s.post("https://cas2.uvsq.fr/cas/login?service=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2Fservices%2FdoAuth.php%3Fhref%3Dhttps%253A%252F%252Fbulletins.iut-velizy.uvsq.fr%252F", data = data, verify=True)

request = s.get("https://bulletins.iut-velizy.uvsq.fr/services/doAuth.php?href=https%3A%2F%2Fbulletins.iut-velizy.uvsq.fr%2F", verify=True)

request_html = BeautifulSoup(request.text, 'html.parser')
notes_request = s.get("https://bulletins.iut-velizy.uvsq.fr/services/data.php?q=relev%C3%A9Etudiant&semestre=415", verify=True)
notes = json.loads(notes_request.text)

print("\n")

data = {
    'ressources': {
        'BRT2UE1':{
        },
        'BRT2UE2':{
        },
        'BRT2UE3':{
        }
    },
    'ues': {
        'BRT2UE1':{
        },
        'BRT2UE2':{
        },
        'BRT2UE3':{
        }
    },
    'absences': {

    }
}

colors = ["#ca1414", "#ca1414", "#ca1414", "#ca1414", "#ea1818", "#ea1818", "#ea1818", "#ea1818", "#eb6b17", "#ebb117", "#ebe117", "#e5eb17", "#d8eb17", "#cbeb17","#bfeb17", "#9feb17", "#6ceb17", "#2dde15", "#28c513", "#13be7f", "#7013bf"]

for ue in notes['relevé']['ues']:
    moyennes = []
    coeffs = []
    coef_total = 0
    moyenne_total = 0
    for r in notes['relevé']['ues'][ue]['ressources']:
        data["ressources"][ue][r] = {}
        data["ressources"][ue][r]["titre"] = notes['relevé']['ressources'][r]['titre']
        cof = float(notes['relevé']['ues'][ue]['ressources'][r]['coef'])
        if not notes['relevé']['ues'][ue]['ressources'][r]['moyenne'] == "~":
            moy = float(notes['relevé']['ues'][ue]['ressources'][r]['moyenne'])
            data["ressources"][ue][r]["moyenne"] = moy
            data["ressources"][ue][r]["coeff"] = cof
            data["ressources"][ue][r]["couleur"] = colors[int(moy)]
            moyennes.append(moy*cof)
            coeffs.append(cof)
        else:
            data["ressources"][ue][r]["moyenne"] = 0
            data["ressources"][ue][r]["coeff"] = cof
            data["ressources"][ue][r]["couleur"] = "#000000"

    for sae in notes['relevé']['ues'][ue]['saes']:
        data["ressources"][ue][sae] = {}
        data["ressources"][ue][sae]["titre"] = notes['relevé']['saes'][sae]['titre']
        cof = float(notes['relevé']['ues'][ue]['saes'][sae]['coef'])
        if not notes['relevé']['ues'][ue]['saes'][sae]['moyenne'] == "~":
            moy = float(notes['relevé']['ues'][ue]['saes'][sae]['moyenne'])
            data["ressources"][ue][sae]["moyenne"] = moy
            data["ressources"][ue][sae]["coeff"] = cof
            data["ressources"][ue][sae]["couleur"] = colors[int(moy)]
            moyennes.append(moy*cof)
            coeffs.append(cof)
        else:
            data["ressources"][ue][sae]["moyenne"] = 0
            data["ressources"][ue][sae]["coeff"] = cof
            data["ressources"][ue][sae]["couleur"] = "#000000"

    for c in coeffs:
        coef_total += c
        
    for m in moyennes:
        moyenne_total += m

    if coef_total > 0:
        moyenne_ue = round(moyenne_total/coef_total, 2)
        data["ues"][ue]["moyenne"] = moyenne_ue
        data["ues"][ue]["titre"] = notes['relevé']['ues'][ue]['titre']
        data["ues"][ue]["couleur"] = colors[int(moyenne_ue)]
        print(ue + " : " + str(moyenne_ue))
    else:
        print(ue + " : ~ ")

absences = notes['relevé']['semestre']['absences']['total']
absences_injustifiées = notes['relevé']['semestre']['absences']['injustifie']
data["absences"]["total"] = absences
data["absences"]["injustifie"] = absences_injustifiées

with open("notes.json", "w") as notes_file:
    json.dump(data, notes_file)
    notes_file.close()

print("\nAbsences injustifiées : " + str(absences_injustifiées) + "/" + str(absences))

input("Appuyer sur Entrez pour sortir...")
