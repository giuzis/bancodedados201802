from xml.dom.minidom import parse
import xml.dom.minidom
import os
import csv

# Abre o XML com o minidom parser
DOMTree = xml.dom.minidom.parse("marvel_simplificado.xml")

universe = DOMTree.documentElement

# Pega todos os herois do universo
heroes = universe.getElementsByTagName("hero")

numero_herois = 0
numero_bons = 0
numero_maus = 0
peso = 0
peso_hulk = 0
altura_hulk = 0

# Pega as informações dos herois
for hero in heroes:
   name = hero.getElementsByTagName('name')[0]
   popularity = hero.getElementsByTagName('popularity')[0]
   alignment = hero.getElementsByTagName('alignment')[0]
   gender = hero.getElementsByTagName('gender')[0]
   height_m = hero.getElementsByTagName('height_m')[0]
   weight_kg = hero.getElementsByTagName('weight_kg')[0]
   hometown = hero.getElementsByTagName('hometown')[0]
   intelligence = hero.getElementsByTagName('intelligence')[0]
   strength = hero.getElementsByTagName('strength')[0]
   speed = hero.getElementsByTagName('speed')[0]
   durability = hero.getElementsByTagName('durability')[0]
   energy_Projection = hero.getElementsByTagName('energy_Projection')[0]
   fighting_Skills = hero.getElementsByTagName('fighting_Skills')[0]

   # Conta o numero de herois somando a cada iteração
   numero_herois += 1

   # Coleta as informações do Hulk
   if name.childNodes[0].data == 'Hulk':
      peso_hulk += int(weight_kg.childNodes[0].data)
      altura_hulk += int(height_m.childNodes[0].data)

   # Soma os pesos de cada heroi a cada iteração
   peso += int(weight_kg.childNodes[0].data)

   # Soma o numero de herois bons/maus a cada iteração
   if alignment.childNodes[0].data == 'Good':
      numero_bons += 1
   elif alignment.childNodes[0].data == 'Bad':
      numero_maus += 1


proporcao = numero_bons/numero_maus
print("Proporção Bons/Maus %s" % proporcao)
media = peso/numero_herois
print("Media dos pesos: %s" % media)
mmc_hulk = peso_hulk/(altura_hulk**2)
print("MMC do Hulk: %s" % mmc_hulk)

# Cria pasta dadosMarvel
newpath = r'/home/alexandre/Documentos/dadosMarvel'
os.makedirs(newpath)



