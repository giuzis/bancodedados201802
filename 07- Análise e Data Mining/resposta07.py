#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2;
import psycopg2.extras;
import psycopg2.extensions
import os
import subprocess
import csv
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#Métodos/Funções

def calcula_media(coluna,tabela):
	#e_coluna => coluna externo;
	#e_tabela => tabela externa;
	sql_media = str("SELECT AVG(coluna_tb) AS Media FROM tabela_tb ;")
	sql_media = sql_media.replace ("coluna_tb",coluna)
	sql_media = sql_media.replace ("tabela_tb",tabela)

	#Executa a query
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
		cur.execute(sql_media)
		print("Media")
		for media in cur:
			print(unicode(media[0]))
	except:
		print("Falha na pesquisa")
	conn.commit()
	cur.close()

def calcula_desvio(coluna,tabela):
	#e_coluna => coluna externo;
	#e_tabela => tabela externa;
	sql_desvio = "SELECT STDDEV(coluna_tb) AS DesvioPadrao FROM tabela_tb ;"
	sql_desvio = sql_desvio.replace ("coluna_tb",coluna)
	sql_desvio = sql_desvio.replace ("tabela_tb",tabela)

	#Executa a query
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
		cur.execute(sql_desvio)
		print("Desvio")
		for desvio in cur:
			print(unicode(desvio[0]))
	except:
		print("Falha na pesquisa")
	conn.commit()

def conheceNormalizada(): #4
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
		cur.execute("DROP VIEW ConheceNormalizada CASCADE;")
		conn.commit()
	except:
		pass

	conn.rollback()
	cur.execute("create or replace view ConheceNormalizada as select p1.login as login1, p2.login as login2 from pessoa p1, pessoa p2, conhece where (p1.login=conhece.login1 and p2.login=conhece.login2) or (p1.login=conhece.login2 and p2.login=conhece.login1)	group by p1.login, p2.login;")
	conn.commit()
	cur.close()
	print
	print "VIEW criada com o nome de ConheceNormalizada"

def compartilhaMaxFilmes(): #5
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
		cur.execute("DROP VIEW compartilhaMax;")
	except:
		pass
	conn.rollback()
	cur.execute("create or replace view compartilhaMax as (select con.login1 as l1, con.login2 as l2, c1.num+c2.num as soma from ConheceNormalizada con, (select login, count(login) as num from like_filmes GROUP BY login) as c1, (select login, count(login) as num from like_filmes GROUP BY login) as c2 where con.login1 = c1.login and con.login2=c2.login); ")
	conn.commit()
	conn.rollback()
	cur.execute("SELECT l1, l2 from compartilhaMax where soma in (select max(soma) from compartilhaMax);")
	resp = cur.fetchone()
	print
	print"Pessoas que compartilham maior quantidade de filmes:"
	print str(resp[0])
	print str(resp[1])

	cur.close()

def conhecidosConhecidos(): #6
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	conn.rollback()
	cur.execute("select con1, count(con1) as num_con from (select DISTINCT c2.login1 as con1, c2.login2 as con2 from ConheceNormalizada c1, ConheceNormalizada c2 where c1.login1 in ('DI1802giulianasilva', 'DI1802alexandrematias', 'DI1802matheusoliveira') and c1.login2 = c2.login1) as conhecidos2 GROUP BY con1;")
	resp = cur.fetchall()
	print "soma dos conhecidos dos conhecidos:"
	for i in resp:
		print str(i[0])+" "+str(i[1]) 
	
	cur.close()



def graficoFilmesPessoas():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	eixoX = []
	eixoY = []
	try:
		#cur.execute("CREATE VIEW num AS SELECT COUNT(like_filmes.login) FROM like_filmes GROUP BY like_filmes.login;")
		#conn.commit()
		cur.execute("SELECT count, count(*) AS quantpessoas FROM num GROUP BY count;")
		for nota in cur:
			eixoX.append(str(nota[0]))
			eixoY.append(str(nota[1]))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()
	zip(eixoX, eixoY)
	with open("dadosGnuoplotFilmesPessoas.csv", "w") as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerows(zip(eixoX, eixoY))
	comandosGnuplot = open("comandosGnuplotFilmesPessoas.txt", "wt")
	comandosGnuplot.write("plot 'dadosGnuoplotFilmesPessoas.csv' using 1:2 with lines title 'Numero de Pessoas que Curtiram x Numero de Filmes'\n")
	comandosGnuplot.write("set term png\nset output 'graficoFilmesPessoas.png'\nreplot\nset term x11\n")
	p = subprocess.Popen("gnuplot -p comandosGnuplotFilmesPessoas.txt", shell = True)
	os.waitpid(p.pid, 11)

def graficoPessoasFilmes():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	eixoX = []
	eixoY = []
	try:
		#cur.execute("CREATE VIEW num2 AS SELECT COUNT(like_filmes.id) FROM like_filmes GROUP BY like_filmes.id;")
		#conn.commit()
		cur.execute("SELECT count, count(*) AS numpessoas FROM num2 GROUP BY count ORDER BY count;")
		for nota in cur:
			eixoX.append(str(nota[0]))
			eixoY.append(str(nota[1]))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()
	zip(eixoX, eixoY)
	with open("dadosGnuoplotPessoasFilmes.csv", "w") as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerows(zip(eixoX, eixoY))
	comandosGnuplot = open("comandosGnuplotPessoasFilmes.txt", "wt")
	comandosGnuplot.write("plot 'dadosGnuoplotPessoasFilmes.csv' using 1:2 with lines title 'Numero de Filmes que Foram Curtidos x Numero de Pessoas'\n")
	comandosGnuplot.write("set term png\nset output 'graficoPessoasFilmes.png'\nreplot\nset term x11\n")
	p = subprocess.Popen("gnuplot -p comandosGnuplotPessoasFilmes.txt", shell = True)
	os.waitpid(p.pid, 11)

def makeViewArtistas():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_view = "CREATE VIEW artistas_por_like AS SELECT  artista_musical.nome_artistico,  artista_musical.id, COUNT(artista_musical.nome_artistico) AS num_curtidas FROM artista_musical, like_artista WHERE artista_musical.id = like_artista.id GROUP BY artista_musical.nome_artistico, artista_musical.id ORDER BY artista_musical.nome_artistico;"
	try:
		cur.execute("DROP VIEW artistas_por_like") #Garante que a view desatualizada desapareça.
		cur.execute(sql_view) #Executa a nova view.
		for media in cur:
			print( unicode( unicode(media[0]) + ",  " + unicode(media[1]) ) )
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def makeViewFilmes():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_view = "CREATE VIEW filmes_por_like AS SELECT  filmes.id, COUNT(filmes.id) AS num_curtidas FROM filmes, like_filmes WHERE filmes.id = like_filmes.id GROUP BY  filmes.id;"
	try:
		cur.execute("DROP VIEW filmes_por_like") #Garante que a view desatualizada desapareça.
		cur.execute(sql_view) #Executa a nova view.
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()


def ratingArtistas():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_artista.nota),3) AS Media, artistas_por_like.nome_artistico FROM like_artista, artistas_por_like WHERE  like_artista.id = artistas_por_like.id AND artistas_por_like.num_curtidas >= 2 GROUP BY artistas_por_like.nome_artistico ORDER BY media DESC;"
	makeViewArtistas()
	try:
		cur.execute(sql_run)
		for media in cur:
			print( unicode( unicode(media[0]) + ",  " + unicode(media[1]) ) )
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def ratingFilmes():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_filmes.nota),3) AS Media, filmes_por_like.id FROM like_filmes, filmes_por_like WHERE like_filmes.id = filmes_por_like.id AND filmes_por_like.num_curtidas >=2 GROUP BY filmes_por_like.id ORDER BY media DESC;"
	makeViewFilmes()
	try:
		cur.execute(sql_run) #Executa a query.
		for media in cur:
			print(unicode(unicode(media[0]) + ",  " + unicode(media[1])))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def top10Artistas():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_artista.nota),3) AS Media, artistas_por_like.nome_artistico FROM like_artista, artistas_por_like WHERE  like_artista.id = artistas_por_like.id AND artistas_por_like.num_curtidas >= 2 GROUP BY artistas_por_like.nome_artistico ORDER BY Media DESC LIMIT 10;"
	makeViewFilmes()
	try:
		cur.execute(sql_run)
		for media in cur:
			print(unicode(unicode(media[0]) + ",  " + unicode(media[1])))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def top10Filmes():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_filmes.nota),3) AS Media, filmes_por_like.id FROM like_filmes, filmes_por_like WHERE like_filmes.id = filmes_por_like.id AND filmes_por_like.num_curtidas >=2 GROUP BY (filmes_por_like.id)  ORDER BY media DESC LIMIT 10;"
	makeViewFilmes()
	try:
		cur.execute(sql_run)
		for media in cur:
			print(unicode(unicode(media[0]) + ",  " + unicode(media[1])))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def bot10Artistas():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_artista.nota),3) AS Media, artistas_por_like.nome_artistico FROM like_artista, artistas_por_like WHERE  like_artista.id = artistas_por_like.id AND artistas_por_like.num_curtidas >= 2 GROUP BY artistas_por_like.nome_artistico ORDER BY Media LIMIT 10;"
	makeViewFilmes()
	try:
		cur.execute(sql_run)
		for media in cur:
			print(unicode(unicode(media[0]) + ",  " + unicode(media[1])))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()

def bot10Filmes():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql_run = "SELECT ROUND(AVG(like_filmes.nota),3) AS Media, filmes_por_like.id FROM like_filmes, filmes_por_like WHERE like_filmes.id = filmes_por_like.id AND filmes_por_like.num_curtidas >=2 GROUP BY (filmes_por_like.id)  ORDER BY media LIMIT 10;"
	makeViewFilmes()
	try:
		cur.execute(sql_run)
		for media in cur:
			print(unicode(unicode(media[0]) + ",  " + unicode(media[1])))
	except Exception as e:
		print("Falha na pesquisa")
		print e
	conn.commit()
	cur.close()
#Variáveis de controle de menu.
end = False;
menu = True;

#Conexão com o banco.
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'") #Envia as informações para se conectar ao banco.
except:
	print("Falha ao se conectar ao banco de dados.")
	end = True; #Controla o while do programa.

while menu and not end:
	#Opções do Menu. Foram separadas em diferentes prints para melhor visualização.
	print("Bem vindo! O que deseja fazer? \n")
	print("1 - Fechar o programa.")
	print("2 - Calcular Média e Desvio Padrão dos ratings. (De Artistas Musicais e ou Filmes).")
	print("3 - Obter Artistas  Musicais e Filmes com o maior rating médio. ")
	print("4 - TOP 10 Artistas Musicais e Filmes mais populares ")
	print("5 - Descubra quem é seu amigo de verdade! ")
	print("6 - Descubra os filmes mais curtidos pelos seus amigos ")
	print("7 - Descubre os conhecidos dos seus conhecidos. ")
	print("8 - Gráfico: Filmes vs Curtidas ")
	print("9 - Gráfico: Quantidade de filmes curtidos vs Pessoas ")
	print("10 - TOP 10 Artistas Musicais menos populares")
	print("11 - TOP 10 Filmes menos populares ")
	option = raw_input("Selecione a opção desejada: ")
	if option=="1":
		print("\n Fechando o programa... \n")
		menu = False
	elif option=="2":
		#print("Qual é a média e desvio padrão dos ratings para artistas musicais e filmes?")
		menu_in = True;
		while menu_in:
			print("O que deseja fazer agora?")
			print("1 - Voltar. \n")
			print("2 - Obter Média e Desvio Padrão dos Artistas Musicais.")
			print("3 - Obter Média e Desvio Padrão dos Filmes.")
			option = raw_input("O que deseja fazer?")
			if option=="1":
				menu_in = False;
			elif option=="2":
				calcula_media("like_artista.nota","like_artista")
				calcula_desvio("like_artista.nota","like_artista")
			elif option=="3":
				calcula_media("like_filmes.nota","like_filmes")
				calcula_desvio("like_filmes.nota","like_filmes")
			else:
				print("Digite uma opção válida!")
	elif option=="3":
		menu_in = True;
		while menu_in:
			print("O que deseja fazer agora?")
			print("1 - Voltar. \n")
			print("2 - Obter Artistas Musicais com maior rating médio (2 pessoas ou + que avaliaram, apenas).")
			print("3 - Obter Filmes com maior rating médio (2 pessoas ou + que avaliaram, apenas).")
			option = raw_input("O que deseja fazer?")
			if option=="1":
				menu_in = False;
			elif option=="2":
				ratingArtistas()
			elif option=="3":
				ratingFilmes()
			else:
				print("Digite uma opção válida!")
	elif option=="4":
		menu_in = True;
		while menu_in:
			print("O que deseja fazer agora?")
			print("1 - Voltar. \n")
			print("2 - Obter TOP 10 Artistas Musicais com maior rating médio (2 pessoas ou + que avaliaram, apenas).")
			print("3 - Obter TOP 10 Filmes com maior rating médio (2 pessoas ou + que avaliaram, apenas).")
			option = raw_input("O que deseja fazer?")
			if option=="1":
				menu_in = False;
			elif option=="2":
				top10Artistas()
			elif option=="3":
				top10Filmes()
			else:
				print("Digite uma opção válida!")
	elif option=="5":
		conheceNormalizada()
	elif option=="6":
		compartilhaMaxFilmes()
	elif option=="7":
    		conhecidosConhecidos()
	elif option=="8":
    		print("Construa um gráfico para a função f(x) = (número de pessoas que curtiram exatamente x filmes).")
    		graficoFilmesPessoas()
	elif option=="9":
    		print("Construa um gráfico para a função f(x) = (número de filmes curtidos por exatamente x pessoas).")
    		graficoPessoasFilmes()
	elif option=="10":
		print("TOP 10 Artistas Musicais com menor rating médio (2 pessoas ou + que avaliaram, apenas).")
		bot10Artistas()
	elif option=="11":
		print("TOP 10 Filmes com menor rating médio (2 pessoas ou + que avaliaram, apenas).")
		bot10Filmes()
	else:
		print("Digite uma opção válida!")


