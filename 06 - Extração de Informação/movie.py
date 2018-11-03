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
	nome_s = nome_s.replace("'","")
	update = update.replace("nome_s", nome_s)
	update = update.replace("data_s", data_s)
	update = update.replace("categoria_s", categoria_s)
	update = update.replace("id_s", id_s)
	return update;

def atualizar_categoria(categoria_s):
	update = "insert into categoria (nome) values ('categoria_s');"
	update = update.replace("categoria_s", categoria_s)
	return update;

def procurar_categoria(categoria_s):
	search = "select * from categoria where nome = 'categoria_s';"
	search = search.replace("categoria_s", categoria_s)
	return search;

def insere_no_arquivo(arquivo,id_s,nome_s,data_s,categoria_s, diretor_s):
	dados_filme = '\t<Movie id="id_s" nome = "nome_s" categoria = "categoria_s" ano_lancamento = "data_s" diretor = "diretor_s" />\n'
	nome_s = nome_s.replace("'","")
	dados_filme = dados_filme.replace("nome_s", nome_s)
	dados_filme = dados_filme.replace("data_s", data_s)
	dados_filme = dados_filme.replace("categoria_s", categoria_s)
	dados_filme = dados_filme.replace("id_s", id_s)
	dados_filme = dados_filme.replace("diretor_s", diretor_s)
	arquivo.write(dados_filme)

#Inicializa a classe Filmes
arquivo = open("movie.xml","w")
arquivo.write('<Movies>\n')

ia = IMDb()
connection.set_client_encoding('LATIN9') #Não sei o que faz, mas coloquei.
cur = connection.cursor() #Se conecta ao banco.s
try:
	cur.execute("SELECT id FROM filmes;") #Testa a execução do SQL da função Listagem.
	cur2 = connection.cursor()
	cur3 = connection.cursor()
	for filme in cur:
		id_filme = filme[0][2:]
		filmes_imdb= ia.get_movie(id_filme)
		try:
			cur2.execute(procurar_categoria(filmes_imdb['genres'][0]))
			verifica = cur2.fetchall()
			if len(verifica) == 0:
				cur3.execute(atualizar_categoria(filmes_imdb['genres'][0]))
				print("Nova insercao da categoria", filmes_imdb['genres'][0])
			else:
				print("Categoria", filmes_imdb['genres'][0], "já inserida.")
		except:
			print("Erro ao procurar categoria.")
			
		try:
			cur3.execute(atualizar_filme(id_filme,filmes_imdb['title'],str(filmes_imdb['year']),filmes_imdb['genres'][0]))
			insere_no_arquivo(arquivo,id_filme,filmes_imdb['title'],str(filmes_imdb['year']),filmes_imdb['genres'][0],filmes_imdb['directors'][0]['name'])
			print("Filme", filmes_imdb['title'], "inserido.")
		except:
			print("Erro ao inserir ou atualizar filme", filmes_imdb['title'])

except: #Se der falha na execução do SQL
	print("Falha ao Listar.")
connection.commit() # efetiva as transações
cur.close() #Fecha o cur.

arquivo.write('</Movies>')

arquivo.close()



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