# Receptari culinari d'Hogarmania

##  Descripció

Aquest repositori conté el codi, dades i respostes per a la realització de la pràctica 1 de l'assignatura "Tipologia i cicle de vida de les dades" del Màster en Ciència de Dades de la Universitat Oberta de Catalunya. La pràctica elaborada consisteix en la implementació de tècniques de web scraping per a la creació d'un dataset amb informació i dades per a la creació d'un receptari culinari a partir de les dades extretes del web www.hogarmania.com
Podeu trobar més informació al pdf adjunt (PRAC1.pdf)

## Membres de l'equip

Les diferents tasques de la pràctica (i.e. recerca, desenvolupament de codi, redacció, etc) han estat elaborades de manera igualitaria per part dels alumnes Aleix Arnau Soler (aarnauso; @github/AleixArnauSoler) i Adrià Tarradas Planella (atarradasp; @github/latp)

## Fixers disponibles

Aqui trobareu els seguents fitxers:

- **README.md**: informació sobre el repositori i fitxers disponibles.
- **src/receptari_hogarmania.py**: script en llenguatge python per a dur a terme l'extracció de totes les receptes dispnibles a l'apartat de receptes de la secció de cuina de lloc web de 'hogarmania'.
- **data/receptari_hogarmaia_20201109_180010.csv**: dataset generat a partir d'executar l'script "receptari_hogarmania.py". Aquest dataset conté informació de més de 10.000 receptes culinaries (extretes del lloc web a dia specifical al nom del fitxer).
- **PRAC1.pdf**: aquest fitxer conté les respostes de l'anunciat de la pràctica.
- **PRAC1.Rmd**: aquest fitxer conté el codi markdown per a generar el fitxer pdf (PRAC1.pdf).
- **robots.txt**: fitxer "robots.txt" del lloc web (www.hogarmania.com).

## DOI a les dades

El dataset es troba disponible en format CSV a Zenodo amb el DOI:10.5281/zenodo.4265137 (https://doi.org/10.5281/zenodo.4265137)

## Execució del codi

El codi està elaborat en llenguatge Python. Per a la correcta execució del codi, cal tenir instalat in seguit de moduls que, sino estan instalats, podeu instalar a través de 'pip' executant el següen codi:

```
pip install requests
pip install BeatifulSoup
pip install whois
pip install csv
pip install sys
pip install time
pip install io
```
Per a executar l'script i obtenir el dataset complet simplement executi:
```
python receptari_hogarmania.py -scrapper
```
Per a obtenir informacó sobre el propietari del lloc web pot executar:
```
python receptari_hogarmania.py -owner
```
# Bibliografia

- Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
- Masip, D. El lenguaje Python. Editorial UOC.
- Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
- Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
