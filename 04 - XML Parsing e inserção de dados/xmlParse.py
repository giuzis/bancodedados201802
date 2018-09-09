#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import urllib.request

Pessoas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/person.xml'
Artistas_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/music.xml'
Filmes_url = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/movie.xml'
Conhecidos = 'http://dainf.ct.utfpr.edu.br/~gomesjr/BD1/data/knows.xml'


# Parte 1 - Leitura de Pessoas
DOMTree = xml.dom.minidom.parse(urllib.request.urlopen(Pessoas_url))
pessoas = DOMTree.documentElement

turma = pessoas.getElementsByTagName("person")
for person in turma:
	name =  turma.getElementsByTagName('name')[0]
	print ("Nome: %s" % name.childNodes[7].data)	

	me mata senhor