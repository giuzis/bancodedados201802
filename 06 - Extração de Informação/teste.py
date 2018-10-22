#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imdb import IMDb
import psycopg2
#For Special Characters
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#Conecta ao banco de dados
try:
	connection = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
	print("concluido")
except:
	print("Falha ao se conectar ao banco de dados.")

#Métodos
#Realiza uma lista simples
def listagem(column, table):
	lista = "SELECT column FROM table;"
	return lista;

def atualizar(tabela,id_s,nome_s,data_s,categoria_s):
	update = "UPDATE table SET nome ='nome_s', data_de_lançamento = 'data_s', categoria = 'categoria_s' WHERE id='id_s';"
	return update;

def remove_tt(id):
	id = filme.replace("tt","")
	return id;

#Inicializa a classe Filmes
filmes_imdb = IMDb()
cur = connection.cursor() #Se conecta ao banco.
try:
	cur.execute(listagem('id','filmes')) #Testa a execução do SQL da função Listagem.
	for x in cur:
		x = remove_tt(x) #remove os tts dos ids.
		atualizar('filmes',x,filmes_imdb.get_movie(x),filmes_imdb['date'])
except: #Se der falha na execução do SQL
	print("Falha ao Listar.")
	connection.commit() #Não sei o que faz mas precisa.
	cur.close() #Fecha o cur.


#Teste
ia = IMDb()
print(ia.get_movie_infoset())
#print(ia.get_person_infoset())
test = ia.get_movie('0133093')
nome = test['main']
#print(ator)
#ia.update(test, info=['actor'])
#test.current_info