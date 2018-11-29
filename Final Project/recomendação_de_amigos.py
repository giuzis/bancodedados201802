"link uteis"
#https://www.youtube.com/watch?v=8lqUy7RnLFQ&fbclid=IwAR3OyoRTo3BNNEU4dJSFe31P6d6GEn5rR0gq5l4kho9qzcpFRzyZhylPDJs
#https://www.youtube.com/watch?v=K5JT9OyQzbg
#https://medium.com/recombee-blog/machine-learning-for-recommender-systems-part-1-algorithms-evaluation-and-cold-start-6f696683d0ed
#https://github.com/JuliaKikuye/meetup_machine_learning_recsys
#https://docs.scipy.org/doc/numpy/user/quickstart.html
#https://docs.scipy.org/doc/numpy/user/quickstart.html
#https://bcc.ime.usp.br/tccs/2014/marcost/monografia_final.pdf

import psycopg2
import numpy as np
import igraph
from igraph import *

#Conecta ao banco de dados
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

#Obtem o numero de usuarios para a criacao da matriz
def obtemNumeroDeUsuarios(conn):
	cur = conn.cursor()
	consulta = str("select count(*) from pessoa;")
	cur.execute(consulta)
	num_usuario = cur.fetchone()
	cur.close()
	return num_usuario[0];

def obtemAmigosDaPessoa(conn, num_s):
	cur = conn.cursor()
	consulta = str("select amigo2 from num_amigos where amigo1 = num_s;")
	consulta = consulta.replace("num_s", str(num_s))
	cur.execute(consulta)
	num_usuario = cur.fetchall()
	cur.close()
	return num_usuario;

def quemEhEssaPessoa(conn, num_s):
	cur = conn.cursor()
	consulta = str("select login from num_usuario where num = num_s;")
	consulta = consulta.replace("num_s", str(num_s))
	cur.execute(consulta)
	num_usuario = cur.fetchone()
	cur.close()
	return num_usuario[0];

def quantosAmigosEssaPessoaTem(num_s):
	cur = conn.cursor()
	consulta = str("select count(*) from num_amigos where amigo1 = num_s;")
	consulta = consulta.replace("num_s", str(num_s))
	cur.execute(consulta)
	num_usuario = cur.fetchone()
	cur.close()
	return num_usuario[0];

#Essa view sera usada para fazer a associacao de um usuario a um numero
def criaViewNumUsuario(conn):
	cur = conn.cursor()
	consulta = str("create or replace view num_usuario as select -1+row_number() over(order by pessoa) as num, login from pessoa;");
	cur.execute(consulta)
	cur.close()

def criaViewConheceNormalizada(conn):
	cur = conn.cursor()
	consulta = str("create or replace view ConheceNormalizada as select login1, login2 from conhece where login1<login2;");
	cur.execute(consulta)
	cur.close()

#Essa view sera usada para fazer a associacao de um usuario a um numero
def criaViewNumAmigos(conn):
	criaViewConheceNormalizada(conn)
	cur = conn.cursor()
	consulta = str("create or replace view num_amigos as select pessoa1.num as amigo1, pessoa2.num as amigo2 from num_usuario pessoa1, num_usuario pessoa2, ConheceNormalizada conhece where pessoa1.login = conhece.login1 and pessoa2.login = conhece.login2;");
	cur.execute(consulta)
	cur.close()

def preencheGrafo(conn):
	g = Graph()
	total_usuarios = obtemNumeroDeUsuarios(conn)
	g.add_vertices(total_usuarios)  
	for num_pessoa in range(0,total_usuarios):
		todos_amigos = obtemAmigosDaPessoa(conn,num_pessoa)
		g.vs[num_pessoa]["name"] = quemEhEssaPessoa(conn, num_pessoa)
		for amigo in todos_amigos:
			ami = amigo[0]
			g.add_edges([(num_pessoa, ami)])

	# layout = g.layout("kk")
	# g.vs["label"] = g.vs["name"]
	# plot(g, layout = layout, bbox = (1920, 1080), margin = 20, vertex_color = "blue")
	return g

criaViewNumAmigos(conn)
criaViewNumUsuario(conn)
g = preencheGrafo(conn)
id = input("Digite a id da pessoa que deseja sugerir amigos: ")
v = g.vs.find(name=id)

vizinhos = g.neighbors(v.index, mode = ALL)

for vizinho in vizinhos:
	vizinhos_do_vizinho = g.neighbors(vizinho, mode = ALL)
	print("São amigos de", g.vs[vizinho]["name"], ":")
	for vizinho_do_vizinho in vizinhos_do_vizinho:
		if vizinho_do_vizinho not in vizinhos:
			if vizinho_do_vizinho != v.index:
				print(g.vs[vizinho_do_vizinho]["name"])