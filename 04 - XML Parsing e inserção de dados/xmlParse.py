#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import urllib
import urllib2
import psycopg2
import psycopg2.extras 

Pessoas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/person.xml'
Artistas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/music.xml'
Filmes_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml'
Conhecidos = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml'


# Parte 1 - Leitura de Pessoas
DOMTree = xml.dom.minidom.parse(urllib.urlopen(Pessoas_url))
Persons = DOMTree.documentElement

turma = Persons.getElementsByTagName("Person")

try:
 	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
 	print "I am unable to connect to the database."

cur = conn.cursor()

for pessoa in turma:
	string = 'http://utfpr.edu.br/CSB30/2018/2/'
	login = "'" + str(pessoa.getAttribute("uri")).replace(string,'') + "'"
	nome = "'" + pessoa.getAttribute("name") + "'"
	cidadenatal = "'" + pessoa.getAttribute("hometown") + "'"
	if (pessoa.getAttribute("hometown") == ''):
		cidadenatal = "NULL"
	datanascimento = "'" + pessoa.getAttribute("birthdate") + "'"
	if (pessoa.getAttribute("birthdate") == ''):
		datanascimento = "NULL"
	try:
 		cur.execute("INSERT INTO pessoa VALUES (" + login + ", " + nome + ", " + cidadenatal + ", " + datanascimento + ");")
	except Exception as e:
 		print "Nao consegui inserir :("
 		print e
 	conn.commit()

DOMTree2 = xml.dom.minidom.parse(urllib.urlopen(Artistas_url))
AllLikesMusic = DOMTree2.documentElement

musicaturma = AllLikesMusic.getElementsByTagName("LikesMusic")

for musica in musicaturma:
	string1 = 'http://utfpr.edu.br/CSB30/2018/2/'
	login = "'" + str(musica.getAttribute("person")).replace(string1,'') + "'"
	nota = musica.getAttribute("rating")
	idbanda = "'" + musica.getAttribute("bandUri") + "'"
	string2 = 'https://en.wikipedia.org/wiki/'
	nomebanda = "'" + str(musica.getAttribute("bandUri")).replace(string2,'') + "'"
	try:
 		cur.execute("INSERT INTO artista_musical VALUES (" + idbanda + ", " + "NULL" + ", " + nomebanda + ", " + "NULL" + ");")
	except Exception as e:
 		print "Nao consegui inserir :("
 		print e
 	conn.commit()
 	try:
 		cur.execute("INSERT INTO like_artista VALUES (" + login + ", " + idbanda + ", " + nota + ");")
	except Exception as e:
 		print "Nao consegui inserir :("
 		print e
 	conn.commit()
	


