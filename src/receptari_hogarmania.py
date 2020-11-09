###############################################
#											  #
#    Tipologia i Cicle de vida de les dades - PRA 1	  #
#											  #
# Aleix Arnau Soler & Adrià Tarradas Planella #
#											  #
#              Novembre de 2020				  #
#											  #
###############################################

# Instalació de llibreries

# pip install requests
# pip install beautifulsoup4
# pip install python-whois
# pip install lxml
# pip install html5lib

# Importació de llibreries i moduls 
import requests
from bs4 import BeautifulSoup
import whois
import csv
import sys
from time import gmtime, strftime
import io

# Declaració de funcions 
"""
	-----------------------------
	recuperar_nom_tipus_recepta()
	-----------------------------
		Retorna un mapa on les claus són el nom en la url de cada tipus de recepta i el valor de cada un d'ells es el nom col·loquial que s'utilitza per identificar-los
"""
def recuperar_nom_tipus_recepta():
	# Inicialitzem el mapa que retornara la funcio
	tipus_receptes = {}
	
	# Guardem a la llista class_sections el nom de les seccions que contenen url i nom de cuiners
	class_sections = ["destacado"]
	for i in range(1,5):
		class_section_act = "zona" + str(i) + "-items"
		class_sections.append(class_section_act)
		
	# Agafem la pagina des d'on podem obtenir el nom de tots els tipus de receptes
	url_tipus = "https://www.hogarmania.com/cocina/recetas/"
	page_tipus = requests.get(url_tipus)
	soup_tipus = BeautifulSoup(page_tipus.content, features="html.parser")

	# Obtenim la posicio des de la qual podem obtenir el tipus de recepta en la url
	first_char = len("/cocina/recetas/")
	
	# Per cada bloc (i tag en el bucle aniuat) n'obtenim informacio del tipus de recepta
	for a in soup_tipus.find_all("section", {"class": [class_sections]}):
		for b in a.find_all(["h2","h1"]):
			# Obtenim el nom del tipus de recepta
			nom_tipus = b.a['title']
			# Obtenim la url del tipus de recepta
			pagina_tipus = b.a['href']
			# Agafem el nom en clau que s'utilitza en la url per accedir al tipus de recepta
			encoded_type = pagina_tipus[first_char:-1]
			# Guardem en el mapa els elements recuperats
			tipus_receptes[encoded_type] = nom_tipus
	
	# Retornem el mapa amb la informacio dels tipus de recepta
	return tipus_receptes


"""
	--------------------------------------------------------
	recuperar_url_receptes(tipus_receptes,map_tipus_recepta)
	--------------------------------------------------------
		Recupera la informacio de totes les receptes i ho escriu a un fitxer csv nou

	> tipus_receptes: Llista de tots els tipus de recepta que es poden recuperar
	> map_tipus_recepta: Mapa que es va actualitzant on la clau es la url de la recepta i el valor el tipus de recepta a la que pertany
"""
def recuperar_url_receptes(tipus_receptes,map_tipus_recepta):
	# Inicialitzem la llista de url de les receptes que retornara la funcio
	url_receptes = []
	# Creem un string amb la url base que tindran les receptes
	url_base = "https://www.hogarmania.com/cocina/recetas/"
	
	# Per cada tipus de recepta
	for tipus in tipus_receptes:
		# Mostrem informacio del tipus de recepta que s'esta recuperant
		print("> Recuperant receptes de tipus \"" + tipus + "\"")
		# Obtenim la part final de la primera url que s'accedira
		url_tipus = url_base + tipus + "/pagina/1"
		# Inicialitzem un objecte per saber quina es la pagina anterior consultada
		page_ant = None
		# Obtenim les dades de la primera pagina i ho guardem a un objecte de tipus bs4
		page_act = BeautifulSoup(requests.get(url_tipus).content, features="html.parser")
		
		# En cas que la pagina existeixi hem accedit a la pagina d'una recepta i per tant en guardem la informacio
		if page_act.find('meta',{'name' : 'keywords'})['content'].find("no existe") == -1:
			# Inicialitzem el nombre de la pagina que es vol recuperar
			num_page = 1
			# Detectem que no cal augmentar mes de pagina quan la pagina anterior es igual que l'actual
			while (page_act != page_ant):
			
				print("  > Recuperant les receptes de la pagina " + str(num_page))
				# Agafem informacio de totes les receptes de la pagina actual
				llistat_receptes = page_act.find('div', {'class' : 'especial listado'})
				# Per cada bloc d'informacio recuperat n'extraiem la url
				for div_recepta in llistat_receptes.find_all('article',{'class' : 'modulo'}):
					url_recepta = div_recepta.a['href']
					# En cas que la referencia a la url de la recepta no sigui absoluta, n'afegim el prefix
					if url_recepta.find('https') == -1:
						url_recepta = 'https://www.hogarmania.com' + url_recepta
					# Actualitzem el mapa per saber a quin tipus pertany la recepta
					map_tipus_recepta[url_recepta] = tipus
					# Afegim la url de la recepta recuperada a la llista de retorn
					url_receptes.append(url_recepta)
				
				print("  > Receptes de la pagina " + str(num_page) + " recuperades")
				# Actualitzem pagina anterior amb el valor de la pagina actual per la comparacio del bucle
				page_ant = page_act
				# Incrementem la pagina
				num_page = num_page + 1
				# Actualitzem la url de la pagina actual 
				url_tipus = url_base + tipus + "/pagina/" + str(num_page)
				# Actualitzem el valor de la pagina actual
				page_act = BeautifulSoup(requests.get(url_tipus).content, features="html.parser")
			
			# Mostrem la quantitat de url de receptes de cada tipus que s'han recuperat
			print("> Receptes de tipus \"" + tipus + "\"" + " recuperades")
			
	# Retornem la llista de url de receptes
	return(url_receptes)


"""
	-------------------------------------------------
	obtenir_receptes(url_receptes,map_tipus_recepta):
	-------------------------------------------------
		Recupera la informacio de totes les receptes i ho escriu a un fitxer csv nou

	> tipus_receptes:	Mapa que conté la url de tots els tipus de recepta
	> url_receptes:		Llistat de totes les url de receptes
"""
def obtenir_receptes(url_receptes, map_tipus_recepta):
	# Creem el nom del fitxer csv a partir de la data actual 
	nom_fitxer = 'receptari_hogarmania_' + strftime("%Y-%m-%d %H:%M:%S", gmtime()).replace(" ", "_").replace("-","").replace(":","") + ".csv"
	
	# Creem el fitxer csv amb codificacio 'utf-8' i evitem que generi 2 salts de linia per cada fila
	fitxer_csv = open(nom_fitxer, 'w', encoding="utf-8", newline='')
	
	# Creem l'objecte que permetra escriure al fitxer i especifiquem que el delimitador dels camps sigui ';'
	escriptor_csv = csv.writer(fitxer_csv, delimiter=';')
	
	# Escrivim al fitxer la capçalera amb els camps del dataset
	escriptor_csv.writerow(["titol","ingredients","temps_preparacio","temps_total","chef","elaboracio","info_nutricional","consells_doctor","link_imatge","link_video_resum","link_video_complet","tipus_recepta","persones"])
	
	# Obtenim la quantitat total de receptes que s'han de recuperar
	n = str(len(url_receptes))
	
	# Inicialitzem la variable 'i' per saber quina recepta s'esta recuperant
	i = 1
	
	print("> Recuperant receptes...")	
	# Obtenim totes les dades de cada recepta
	for url_recepta in url_receptes:
		# Mostrem informacio de la recepta que s'està recuperant
		print("  > Recuperant la recepta " + str(i) + "/" + n + " de " + url_recepta)
		i = i + 1
		
		# Obtenim el tipus de recepta
		tipus_recepta = map_tipus_recepta[url_recepta]
		
		# Demanem la informacio de la recepta a la pagina web
		url_recepta = requests.get(url_recepta)
		soup = BeautifulSoup(url_recepta.content,features="html.parser")

		# Obtenim el titol de la recepta
		main = soup.find("main")
		titol_recepta = main.h1.text
		
		# Obtenim el nombre de persones per les que és la recepta
		persones = "NA"
		try:
			# Obtenim el text del bloc on hi ha la informacio de la quantitat de persones 
			recipe_ingredients = main.find("ul", class_ = "ingredientes")
			text_parent = recipe_ingredients.parent.text
			# Obtenim la posicio dins del text on hi ha la informacio
			posicio_caracter = text_parent.find("Ingredientes (")
			# En cas que hi hagi el nombre de persones
			if posicio_caracter != -1:
				# Eliminem la part inicial del text
				text_parent_aux = text_parent[posicio_caracter+len("Ingredientes ("):]
				# Obtenim la posicio de l'ultim caracter que conte la informacio
				ultim_caracter = text_parent_aux.find(" ")
				if ultim_caracter != -1:
					# Si el valor es resultant es numeric, obtenim la informacio de per a quantes persones es la recepta
					if text_parent_aux[0:ultim_caracter].strip().isdigit():
						persones = text_parent_aux[0:ultim_caracter].strip()
		except:
			pass
			
		# Obtenim els ingredients de la recepta
		try:
			recipe_ingredients = main.find("ul", class_ = "ingredientes")
			ingredients=[]
			for ingredient in recipe_ingredients:
				ingredients.append(ingredient.text)
			ingredients = ', '.join(ingredients)
		except:
			ingredients = "NA"

		# Obtenim el nom del cuiner
		recipe_chef = "NA"
		try:
			recipe_chef = main.find("p", class_ = "autor").a["title"]
		except:
			pass

		# Obtenim les temps total i de preparacio de la recepta
		temps_preparacio_recepta = "NA"
		temps_total_recepta = "NA"
		try:
			temps_recepta = main.find_all("p", class_ = "autor")[2].text
			# Obtenim el temps de preparacio
			temps_preparacio_recepta = temps_recepta.split("|")[0].split(":")[1]
			# Obtneim el temps total
			temps_total_recepta = temps_recepta.split("|")[1].split(":")[1]
		except:
			pass
		
		# Obtenim el temps d'elaboracio
		proces_elaboracio = main.find_all("div",class_ = "articulo")[0].text
		elaboracio_recepta = "NA"
		try:
			elaboracio_recepta = proces_elaboracio.split("Elaboración de la receta")[1].split("Información nutricional")[0]
			elaboracio_recepta = "Elaboracion de la receta" + elaboracio_recepta
		except:
			pass
			
		try:
			elaboracio_recepta = proces_elaboracio.split("Elaboración de la receta")[1].split("Presentación de la receta")[0]
			elaboracio_recepta = "Elaboracion de la receta" + elaboracio_recepta
		except:
			pass	
		
		# Obtenim l'informacio nutricional
		info_nutricional = "NA"
		try:
			info_nutricional = proces_elaboracio.split("Información nutricional de la receta:")[1].split("Consejo de la Doctora")[0]
		except:
			pass

		# Obtenim el consell del doctor
		consell_doctor = "NA"
		try:
			consell_doctor = proces_elaboracio.split("Consejo de la Doctora Telleria:")[1]
		except:
			pass

		# Obtenim el link de la imatge de la recepta
		url_imatge_recepta = "NA"
		try:
			imatges_recepta = main.find("div", class_ ="galeria").img["src"]
			url_imatge_recepta = "https://www.hogarmania.com"+imatges_recepta
		except:
			pass
		
		try:
			imatges_recepta = main.find("div", class_ ="articulo").img["src"]
			url_imatge_recepta = imatges_recepta
		except:
			pass

		# Obtenim el link del video resum
		url_video_resum = "NA"
		try:
			url_video_resum = main.find("iframe")["src"]
		except:
			pass

		# Obtenim el link del video complet
		url_video_complet = "NA"
		try:
			url_video_complet = main.find_all("p", class_ = "autor")[1].a["href"]
		except:
			pass

		# Escrivim la informacio de la recepta al fitxer csv eliminant els espais en blanc inicials i finals de cada valor amb la funcio strip
		escriptor_csv.writerow([titol_recepta.strip(), ingredients.strip(), temps_preparacio_recepta.strip(), temps_total_recepta.strip(), recipe_chef.strip(), elaboracio_recepta.strip(), info_nutricional.strip(), consell_doctor.strip(), url_imatge_recepta.strip(), url_video_resum.strip(), url_video_complet.strip(), tipus_recepta.strip(), persones.strip()])
	
	# Mostrem el total de receptes recuperades
	print("> " + n + " receptes recuperades")


""" 
	--------------------
	scrapper(arguments): 
	--------------------
		Construeix el dataset de 'Receptari hogarmania', recollint totes les url de les receptes, obtenint la informacio de cada una d'elles i guardant-ho a un fitxer csv
"""
def scrapper(argv):
	# Obtenim les url de tots els tipus de receptes
	tipus_receptes = recuperar_nom_tipus_recepta()
	# Creem l'objecte que indicara de quin tipus es cada recepta
	map_tipus_recepta = {}
	# Recuperem la url de totes les receptes i emplenem el mapa per saber de quin tipus es cada recepta
	url_receptes = recuperar_url_receptes(tipus_receptes, map_tipus_recepta)
	# Obtenim la informacio de cada recepta i l'escrivim a un fitxer csv del mateix directori
	obtenir_receptes(url_receptes, map_tipus_recepta)


"""
	Execució per defecte
"""
if __name__ == "__main__":
	# Si no s'inclou un argument mostra com s'ha d'utilitzar el programa
	if len(sys.argv) != 2:
		print("usage: python receptari_hogarmania.py <-owner | -scrapper>")
	else:
		# Si l'argument es '-owner' mostra informacio del propietari de la pagina
		if sys.argv[1] == "-owner":
			print(whois.whois("https://www.hogarmania.com/cocina/recetas/"))
		# Si l'argument es '-scrapper' construeix el dataset de les receptes
		elif sys.argv[1] == "-scrapper":
			scrapper(sys.argv[2:])
		# Si no s'ha inclos cap argument valid mostra com s'ha d'utilitzar el programa
		else:
			print("usage: python receptari_hogarmania.py <-owner | -scrapper>")
