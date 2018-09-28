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
	print("10 - Opção extra 01 ")
	print("11 - Opção extra 02 ")
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
		print("Quais são os artistas e filmes com o maior rating médio curtidos por pelo menos duas pessoas? Ordenados por rating médio.")
	elif option=="4":
		print("Quais são os 10 artistas musicais e filmes mais populares? Ordenados por popularidade.")
	elif option=="5":
		print("Crie uma view chamada ConheceNormalizada que represente simetricamente os relacionamentos de conhecidos da turma. Por exemplo, se a conhece b mas b não declarou conhecer a, a view criada deve conter o relacionamento (b,a) além de (a,b).")
	elif option=="6":
		print(" Quais são os conhecidos (duas pessoas ligadas na view ConheceNormalizada) que compartilham o maior numero de filmes curtidos?")
	elif option=="7":
    		print("Qual o número de conhecidos dos conhecidos (usando ConheceNormalizada) para cada integrante do seu grupo?")
	elif option=="8":
    		print("Construa um gráfico para a função f(x) = (número de pessoas que curtiram exatamente x filmes).")
    		graficoFilmesPessoas()
	elif option=="9":
    		print("Construa um gráfico para a função f(x) = (número de filmes curtidos por exatamente x pessoas).")
    		graficoPessoasFilmes()
	elif option=="10":
		print("Defina duas outras informações (como as anteriores) que seriam úteis para compreender melhor a rede. Agregue estas informações à sua aplicação.")
	elif option=="11":
		print("batata")
	else:
		print("Digite uma opção válida!")


