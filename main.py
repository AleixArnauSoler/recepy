# Importacio de llibreries
import requests
from bs4 import BeautifulSoup

# Agafem tots els cuiners
url_cuniers = "https://www.hogarmania.com/cocina/cocineros/"
page = requests.get(url_cuniers)
soup = BeautifulSoup(page.content)

# Guardem a la llista class_sections el nom de les seccions que contenen url i nom de cuiners
class_sections = ["destacado"]
for i in range(1,5):
	class_section_act = "zona" + str(i) + "-items"
	class_sections.append(class_section_act)

# Obtenim la url i el nom dels cuiners
for a in soup.find_all("section", {"class": [class_sections]}):
	for b in a.find_all(["h2","h1"]):
		print(b.a['title'])
		print(b.a['href'])
		print("\n\n")
		
# Per cada cuiner obtenim totes les url de les seves receptes
