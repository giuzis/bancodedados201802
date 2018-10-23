import json
import urllib
import urllib2
import psycopg2
import psycopg2.extras 
import csv

try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print "Falha ao se conectar ao banco de dados. Terminando o programa..."
	end = True

listamusicas = []
cur = conn.cursor()
try:
	cur.execute("SELECT nome_artistico FROM artista_musical")
	for nomes in cur:
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

			if cantor.find("genre") != -1:
				iniciogenero = cantor.find("genre") + len("genre")
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
			else:
				genero = cantor
				genero = genero.replace("{","")
				genero = genero.replace("}","")
				genero = genero.replace("[","")
				genero = genero.replace("]","")
				genero = genero.replace(" = hlist|","")
				genero = genero[0:genero.find("|")]
				genero = genero.replace("\n","")

			listamusicas.append("https://en.wikipedia.org/wiki/" + nomes[0] + "|" + nome + "|" + cidade + "|" + pais + "|" + genero)
		else:
			banda = string2
			inicionome = banda.find("name") + len("name")
			banda = banda[inicionome:len(banda)]
			nome = banda[0:banda.find("\n")]
			nome = nome[nome.find("=")+2:len(nome)]
			if nome.find("<") != -1:
				nome = nome[0:nome.find("<")]

			iniciopais = banda.find("origin") + len("origin")
			banda = banda[iniciopais:len(banda)]
			pais = banda[0:banda.find("\n")]
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
			elif count == 1:
				cidade,pais = pais.split(",")
			elif count == 2:
				cidade,estado,pais = pais.split(",")
			else:
				pais = "NULL"
			pais = pais[1:len(pais)]

			if banda.find("genre") != -1:
				iniciogenero = banda.find("genre") + len("genre")
			else:
				iniciogenero = banda.find("Genre") + len("Genre")	
			banda = banda[iniciogenero:len(banda)]
			genero = banda[0:banda.find("\n")]
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
				genero = banda
				genero = genero[genero.find("*")+2:len(genero)]
				genero = genero[0:genero.find("\n")]
				genero = genero.replace("[","")
				genero = genero.replace("]","")
				if genero.find("|") != -1:
					genero = genero[0:genero.find("|")]
			else:
				genero = banda
				genero = genero.replace("{","")
				genero = genero.replace("}","")
				genero = genero.replace("[","")
				genero = genero.replace("]","")
				genero = genero.replace(" = hlist|","")
				genero = genero[0:genero.find("|")]
				genero = genero.replace("\n","")

			listamusicas.append("https://en.wikipedia.org/wiki/" + nomes[0] + "|" + nome + "|" + cidade + "|" + pais + "|" + genero)

except Exception as e: 
	print e

file = open("musicas.csv",'w')
for linha in listamusicas:
	file.write("%s\n" % linha.encode('utf-8'))
