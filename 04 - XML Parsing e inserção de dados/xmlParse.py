#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import urllib
import urllib2
import psycopg2
import psycopg2.extras 

Pessoas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/person.xml'
Artistas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/music.xml'
Knows_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml'
Movies_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml'



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
	


knows_data = urllib2.urlopen(Knows_url)
movies_data = urllib2.urlopen(Movies_url)
DOMTree3 = xml.dom.minidom.parse(knows_data)
allKnows = DOMTree3.documentElement

knows = allKnows.getElementsByTagName("Knows")

url_login = 'http://utfpr.edu.br/CSB30/2018/2/'

for person in knows:

	# string para os inserts
	insert_know = "INSERT INTO conhece VALUES ('login1', 'login2');"

	id_person = person.getAttribute('person')
	id_person = id_person.replace(url_login, "")
	id_colleague = person.getAttribute('colleague')
	id_colleague = id_colleague.replace(url_login, "")
	
	insert_know = insert_know.replace("login1", id_person)
	insert_know = insert_know.replace("login2", id_colleague)

	try:
 		cur.execute(insert_know)
	except Exception as e:
 		print "I can't insert_know!"
 		print e
	conn.commit()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

DOMTree4 = xml.dom.minidom.parse(movies_data)
allLikesMovie = DOMTree4.documentElement

likesMovie = allLikesMovie.getElementsByTagName("LikesMovie")

url_imdb = 'http://www.imdb.com/title/'

for likes in likesMovie:

	# string para os inserts
	insert_filme = "INSERT INTO Filmes VALUES ('id_filme');"
	insert_likeFilme = "INSERT INTO Like_Filmes VALUES ('id_person', 'id_filme', nota);"

	id_person = likes.getAttribute('person')
	id_person = id_person.replace(url_login, "")
	id_filme = likes.getAttribute('movieUri')
	id_filme = id_filme.replace(url_imdb, "")
	id_filme = id_filme.replace("/", "")
	nota = likes.getAttribute('rating')
	

	insert_filme = insert_filme.replace("id_filme", id_filme)
	insert_likeFilme = insert_likeFilme.replace("id_person", id_person)
	insert_likeFilme = insert_likeFilme.replace("id_filme", id_filme)
	insert_likeFilme = insert_likeFilme.replace("nota", nota)

	try:
 		cur.execute(insert_filme)
	except Exception as e:
 		print "I can't insert_filme!"
 		print e
	conn.commit()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	try:
 		cur.execute(insert_likeFilme)
	except Exception as e:
 		print "I can't insert_likeFilme!"
 		print e
	conn.commit()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
