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
	update = "UPDATE filmes SET nome = 'nome_s', ano_lancamento = data_s, categoria = 'categoria_s' WHERE id='ttid_s';"
	update = update.replace("nome_s", nome_s)
	update = update.replace("data_s", data_s)
	update = update.replace("categoria_s", categoria_s)
	update = update.replace("id_s", id_s)
	print(update)
	return update;

def atualizar_categoria(categoria_s):
	update = "insert into categoria (nome) values ('categoria_s');"
	update = update.replace("categoria_s", categoria_s)
	print(update)
	return update;

def procurar_categoria(categoria_s):
	search = "select * from categoria where nome = 'categoria_s';"
	search = search.replace("categoria_s", categoria_s)
	print(search)
	return search;

#Inicializa a classe Filmes
ia = IMDb()
connection.set_client_encoding('LATIN9') #Não sei o que faz, mas coloquei.
cur = connection.cursor() #Se conecta ao banco.
try:
	cur.execute("SELECT id FROM filmes;") #Testa a execução do SQL da função Listagem.
	for filme in cur:
		id_filme = filme[0][2:]
		filmes_imdb= ia.get_movie(id_filme)
		try:
			cur.execute(procurar_categoria(filmes_imdb['genres'][0]))
			verifica = cur.fetchall()
			if len(verifica) == 0:
				cur.execute(atualizar_categoria(filmes_imdb['genres'][0]))
				print("Nova insercao da categoria", filmes_imdb['genres'][0])
			else:
				print("Categoria", filmes_imdb['genres'][0], "já inserida.")
		except:
			print("Erro ao procurar categoria.")
			
		try:
			cur.execute(atualizar_filme(id_filme,filmes_imdb['title'],str(filmes_imdb['year']),filmes_imdb['genres'][0]))
		except:
			print("Erro ao inserir ou atualizar filme", filmes_imdb['title'])
			continue
except: #Se der falha na execução do SQL
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