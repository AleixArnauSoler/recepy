# Importacio de llibreries
import requests
from bs4 import BeautifulSoup

# Agafem tots els cuiners
url_cuniers = "https://www.hogarmania.com/cocina/cocineros/"
page = requests.get(url_cuniers)
soup = BeautifulSoup(page.content)
cuiners = {}

# Guardem a la llista class_sections el nom de les seccions que contenen url i nom de cuiners
class_sections = ["destacado"]
for i in range(1,5):
	class_section_act = "zona" + str(i) + "-items"
	class_sections.append(class_section_act)

# Obtenim la url i el nom dels cuiners
for a in soup.find_all("section", {"class": [class_sections]}):
	for b in a.find_all(["h2","h1"]):
		nom_cuiner = b.a['title']
		pagina_cuiner = b.a['href']
		if b.a['href'].find('https') == -1:
			pagina_cuiner = 'https://www.hogarmania.com' + b.a['href']
		cuiners[nom_cuiner] = pagina_cuiner

# Llista dels cuiners		
for cuiner in cuiners:
	# De cada cuiner volem el nom i la pagina per separat
	# Tenim el nom del cuiner i la pagina on te les receptes
	# Agafem les receptes del cuiner i les guardem a un map
	# Recepta:
	#	- Cuiner
	#	- Titol
	# 	- Ingredients
	# 	- Enllaç video
	# 	- 
	#	- 
	
	print(value)
	print(cuiners[value])
	print("\n\n")


# Per cada cuiner obtenim totes les url de les seves receptes
# n'hi ha que tenen nom relatiu i n'hi ha que tenen nom complet
# cal detectar i accedir a la 