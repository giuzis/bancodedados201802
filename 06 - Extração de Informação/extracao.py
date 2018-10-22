import json
import urllib
import urllib2
import psycopg2
import psycopg2.extras
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=Alestorm&format=json"
response = urllib.urlopen(url)
data = json.loads(response.read())
string = data["query"]["pages"]
pageid = []

for letra in string:
	pageid = letra

string2 = data["query"]["pages"][pageid]["revisions"][0]["*"]

indicenomeini = string2.find("name")
indicenomefim = indicenomeini + len("name")

nome = string2[indicenomefim:len(string2)]
fimnome = nome.find("\n")
nome = nome[0:fimnome]
inicionome = nome.find("=")
print nome[inicionome+2:fimnome]

if string2.find("origin"):
	if string2.find("origin") > 0:
		if string2.find("birth_place"):
			if string2.find("origin") < string2.find("birth_place"):
				indicepaisini = string2.find("origin")
				indicepaisfim = indicepaisini + len("origin")
			else:
				indicepaisini = string2.find("birth_place")
				indicepaisfim = indicepaisini + len("birth_place")
		else:
			indicepaisini = string2.find("origin")
			indicepaisfim = indicepaisini + len("origin")
	else:
		indicepaisini = string2.find("birth_place")
		indicepaisfim = indicepaisini + len("birth_place")

origem = string2[indicepaisfim:len(string2)]
print indicepaisfim
fimorigem = origem.find("\n")
origem = origem[0:fimorigem]
inicioorigem = origem.find("=")
novoorigem = origem.replace("[", "")
novonovoorigem = novoorigem.replace("]", "")
if novonovoorigem.find("<"):
	fimorigem = novonovoorigem.find(" <")
	if fimorigem > 0:
		novonovoorigem = novonovoorigem[0:fimorigem]
count = 0
for c in novonovoorigem:
	if c == ",":
		count+=1
print count
if count == 1:
	cidade,pais = novonovoorigem.split(",")
if count == 2:
	cidade,estado,pais = novonovoorigem.split(",")
cidade = cidade.replace("=", "")
countcidade = 0
for c in cidade:
	if c != " ":
		break;
	countcidade+=1
cidade = cidade[countcidade:len(cidade)]
countpais = 0
for c in pais:
	if c != " ":
		break;
	countpais+=1
pais = pais[countpais:len(pais)]
print cidade
print pais

