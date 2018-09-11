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

for pessoa in turma:
	string = 'http://utfpr.edu.br/CSB30/2018/2/'
	login = str(pessoa.getAttribute("uri")).replace(string,'')
	print("login: " + login + ", nome: " + pessoa.getAttribute("name") + ", cidade: " + pessoa.getAttribute("hometown") + ", data de nascimento: " + pessoa.getAttribute("birthdate"))