#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
#import urllib
#import urllib2
import psycopg2
import psycopg2.extras
import requests
from bs4 import BeautifulSoup
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


#Realiza Conexão com o Banco
try:
	connection = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
	print("concluido")
except:
	print("Falha ao se conectar ao banco de dados.")

#Seção de Teste
page = 'https://en.wikipedia.org/wiki/Radiohead'
resposta = get(page)
print(response.text[:500])
soup = BeautifulSoup(page_teste.content, "html.parser")

print soup

#Métodos
#Realiza uma lista simples
def listagem(column, table):
	lista = "SELECT column FROM table;"
	return lista;



#Etapa 1 - Listagem de Filmes;
#connection.set_client_encondig('LATIN9')
#cur = connection.cursor()
#try:
#	cur.execute(listagem('coluna','filmes'));
#except:
#	print("Error")
