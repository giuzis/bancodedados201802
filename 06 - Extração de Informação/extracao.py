import json
import urllib
import urllib2
import psycopg2
import psycopg2.extras
from bs4 import BeautifulSoup

<<<<<<< HEAD
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print "Falha ao se conectar ao banco de dados. Terminando o programa..."
	end = True

cur = conn.cursor()
try:
	cur.execute("SELECT nome_artistico FROM artista_musical")
	for nomes in cur:
		print nomes[0]
		url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=" + nomes[0] + "&format=json"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		string = data["query"]["pages"]
		pageid = []

		for letra in string:
			pageid = letra

		string2 = data["query"]["pages"][pageid]["revisions"][0]["*"]

		string2 = string2[string2.find("Infobox"):len(string2)]

		abre = []
		last_found = -1
		while True:
			last_found = string2.find("{{", last_found + 1)
			if last_found == -1:
				break
			abre.append(last_found)

		fecha = []
		last_found = -1
		while True:
			last_found = string2.find("}}", last_found + 1)
			if last_found == -1:
				break
			fecha.append(last_found)

		valor = 0
		count = 0

		try:
			for coisa1 in fecha:
				if abre[count] > coisa1:
					valor = coisa1
					break
				count += 1
		except:
			valor = fecha[len(fecha)-1]

		string2 = string2[0:valor]

		tipo = string2[len("Infobox")+1:string2.find("\n")]

		if tipo.find("<") > 0:
			tipo = tipo[0:tipo.find("<")]

		if tipo.find("person") != -1:
			cantor = string2
			inicionome = cantor.find("name") + len("name")
			cantor = cantor[inicionome:len(cantor)]
			nome = cantor[0:cantor.find("\n")]
			nome = nome[nome.find("=")+2:len(nome)]
			if nome.find("<") != -1:
				nome = nome[0:nome.find("<")]
			print nome

			iniciopais = cantor.find("birth_place") + len("birth_place")
			cantor = cantor[iniciopais:len(cantor)]
			pais = cantor[0:cantor.find("\n")]
			pais = pais[pais.find("=")+2:len(pais)]
			pais = pais.replace("[","")
			pais = pais.replace("]","")
			if pais.find("<") != -1:
				pais = pais[0:pais.find("<")]
			count = 0
			for c in pais:
				if c == ",":
					count+=1
			if count == 0:
				cidade = "NULL"
				pais = " " + pais
			if count == 1:
				cidade,pais = pais.split(",")
			elif count == 2:
				cidade,estado,pais = pais.split(",")
			else:
				pais = "NULL"
			pais = pais[1:len(pais)]
			print cidade
			print pais

			if cantor.find("genre") != -1:
				iniciogenero = cantor.find("genre") + len("genre")
=======
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
>>>>>>> 2d11f55eb04ede08423b05a1289d0c713dd1fa05
			else:
				iniciogenero = cantor.find("Genre") + len("Genre")	
			cantor = cantor[iniciogenero:len(cantor)]
			genero = cantor[0:cantor.find("\n")]
			genero = genero[genero.find("=")+2:len(genero)]
			if genero.find("<") < genero.find("{") and genero.find("<") != -1:
				genero = genero[genero.find(">"):len(genero)]
			elif genero.find("<") > genero.find("{") and genero.find("<") != -1:
				genero = genero[0:genero.find("<")]
			genero = genero.replace("{","")
			genero = genero.replace("}","")
			genero = genero.replace("[","")
			genero = genero.replace("]","")
			genero = genero[genero.find("flatlist|"):len(genero)]
			genero = genero[0:genero.find("|")]
			if genero.find("flatlist") != -1:
				genero = cantor
				genero = genero[genero.find("*")+2:len(genero)]
				genero = genero[0:genero.find("\n")]
				genero = genero.replace("[","")
				genero = genero.replace("]","")
				if genero.find("|") != -1:
					genero = genero[0:genero.find("|")]
				print genero
			else:
				genero = cantor
				genero = genero.replace("{","")
				genero = genero.replace("}","")
				genero = genero.replace("[","")
				genero = genero.replace("]","")
				genero = genero.replace(" = hlist|","")
				genero = genero[0:genero.find("|")]
				print genero
		else:
<<<<<<< HEAD
			print "nao eh pessoa"

except Exception as e: 
	print e


=======
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
>>>>>>> 2d11f55eb04ede08423b05a1289d0c713dd1fa05

