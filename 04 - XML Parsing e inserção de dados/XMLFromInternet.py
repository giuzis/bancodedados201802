from xml.dom.minidom import parse
import xml.dom.minidom
import urllib
import urllib2
import psycopg2
import psycopg2.extras


# Try to connect
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print "I am unable to connect to the database."

cur = conn.cursor()

Knows_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml'
Movies_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml'

knows_data = urllib2.urlopen(Knows_url)
movies_data = urllib2.urlopen(Movies_url)
DOMTree = xml.dom.minidom.parse(knows_data)
allKnows = DOMTree.documentElement

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

DOMTree2 = xml.dom.minidom.parse(movies_data)
allLikesMovie = DOMTree2.documentElement

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
