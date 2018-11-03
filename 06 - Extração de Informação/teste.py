#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from imdb import IMDb
import psycopg2;
import psycopg2.extras;
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


#Conecta ao banco de dados
try:
	connection = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
	print("concluido")
except:
	print("Falha ao se conectar ao banco de dados.")

#Métodos
#Realiza uma lista simples
def listagem():
	lista = "SELECT ID FROM Filmes;"
	return lista;

def atualizar_filme(id_s,nome_s,data_s,categoria_s):
	update = 'UPDATE filmes SET nome ="nome_s", ano_lancamento = data_s, categoria = "categoria_s" WHERE id="ttid_s";'
	update = update.replace("nome_s", nome_s)
	update = update.replace("data_s", data_s)
	update = update.replace("categoria_s", categoria_s)
	update = update.replace("id_s", id_s)
	return update;

def atualizar_categoria(categoria_s):
	update = "insert into categoria (nome) values ('categoria_s');"
	update = update.replace("categoria_s", categoria_s)
	return update;

#Inicializa a classe Filmes
ia = IMDb()
connection.set_client_encoding('LATIN9') #Não sei o que faz, mas coloquei.
cur = connection.cursor() #Se conecta ao banco.
cur.execute("SELECT id FROM filmes;") #Testa a execução do SQL da função Listagem.
for filme in cur:
	cur1 = connection.cursor()

	id_filme = filme[0][2:]
	filmes_imdb = ia.get_movie(id_filme)
	procura_categoria = "select nome from categoria where nome = 'categoria_s';"
	procura_categoria = procura_categoria.replace("categoria_s", filmes_imdb['genres'][0])
	print(procura_categoria)
	cur1.execute(procura_categoria)
	achou = cur1.fetchall()
	print(achou)
	if len(achou) == 0:
		cur1.execute(atualizar_categoria(filmes_imdb['genres'][0]))
	else:
		print("categoria já inserida")
	
	cur1.execute(atualizar_filme(id_filme,filmes_imdb['title'],str(filmes_imdb['year']),filmes_imdb['genres'][0]))
	print("filme já inserido")
print("Falha ao Listar.")
connection.commit() #Não sei o que faz mas precisa.
cur.close() #Fecha o cur.

"""
#Teste
ia = IMDb()
print(ia.get_movie_infoset())
#print(ia.get_person_infoset())
test = ia.get_movie('0133093')
nome = test['main']
#print(ator)
#ia.update(test, info=['actor'])
#test.current_info
"""