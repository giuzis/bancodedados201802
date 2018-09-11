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
	login = str(pessoa.getAttribute("uri")).replace(string,'')
	if (pessoa.getAttribute("birthdate") == ''):
		try:
 			cur.execute("INSERT INTO pessoa VALUES ('" + login + "', '" + pessoa.getAttribute("name") + "', '" + pessoa.getAttribute("hometown") + "', '20018-01-01');")
		except Exception as e:
 			print "Nao consegui inserir :("
 			print e
 	else:
		try:
 			cur.execute("INSERT INTO pessoa VALUES ('" + login + "', '" + pessoa.getAttribute("name") + "', '" + pessoa.getAttribute("hometown") + "', '" + pessoa.getAttribute("birthdate") + "');")
		except Exception as e:
 			print "Nao consegui inserir :("
 			print e
 	conn.commit()
	