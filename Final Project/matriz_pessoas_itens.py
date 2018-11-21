import psycopg2;
import numpy as np;

#Conecta ao banco de dados
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

#-----------------------------
#Funções

#Encontra a distancia de Jaccard dado conjunto A e B.
def distanciaJaccard(conjuntoA,conjuntoB):
	conjuntoA = set(conjuntoA.split())
	conjuntoB = set(conjuntoB.split())
	coeficiente = len(conjuntoA & conjuntoB)/len(conjuntoA | conjuntoB)
	return 1 - coeficiente;

#Obtem o numero de artistas para a criacao da matriz
def obtemNumeroDeArtistas(conn):
	cur = conn.cursor()
	consulta = str("select count(*) from artista_musical;")
	cur.execute(consulta)
	num_artista = cur.fetchone()
	cur.close()
	return num_artista[0];

#Encontra o número de filmes para criação da Matriz
def encontraNumeroFilmes(conn):
	cur = conn.cursor()
	consulta = "SELECT count(*) FROM Filmes;"
	cur.execute(consulta)
	num_filmes = cur.fetchone()
	cur.close()
	return num_filmes[0];

#Obtem o numero de usuarios para a criacao da matriz
def obtemNumeroDeUsuarios(conn):
	cur = conn.cursor()
	consulta = str("select count(*) from pessoa;")
	cur.execute(consulta)
	num_usuario = cur.fetchone()
	cur.close()
	return num_usuario[0];

#Essa view sera usada para fazer a associacao de um artista a um numero
def criaViewNumArtista(conn):
	cur = conn.cursor()
	consulta = str("create or replace view num_artista as select -1+row_number() over(order by artista_musical) as num, id from artista_musical;");
	cur.execute(consulta)
	cur.close()

#Essa vier sera usada para relacionar filmes a um numero
def criaViewNumFilmes(conn):
	cur = conn.cursor()
	consulta = "CREATE or REPLACE VIEW num_filmes AS SELECT -1+row_number() over(ORDER BY filmes) AS Num, ID FROM Filmes;"
	cur.execute(consulta)
	cur.close()

#Essa view sera usada para fazer a associacao de um usuario a um numero
def criaViewNumUsuario(conn):
	cur = conn.cursor()
	consulta = str("create or replace view num_usuario as select -1+row_number() over(order by pessoa) as num, login from pessoa;");
	cur.execute(consulta)
	cur.close()

#Cria Matriz UsuarioArtista
def criaMatrizUsuarioArtista(conn):
	num_usuario = obtemNumeroDeUsuarios(conn)
	num_artista = obtemNumeroDeArtistas(conn)
	usuario_artista = np.zeros((num_usuario,num_artista))

	return usuario_artista;

#Cria a Matriz UsuariosxFilmes.
def criaMatrizUsuariosxFilmes(conn):
	num_usuario = obtemNumeroDeUsuarios(conn)
	num_filmes = encontraNumeroFilmes(conn)
	usuario_filme = np.zeros((num_usuario,num_filmes))
	return usuario_filme;

def criaMatrizUsuarioxUsuario(conn):
	num_usuario = obtemNumeroDeUsuarios(conn)
	usuario_usuario = np.zeros((num_usuario,num_usuario))
	return usuario_usuario;

#Utiliza as views criadas para preencher a matriz com as notas dadas pelos usuarios
def preencheMatrizUsuarioArtista(conn, num_usuario, usuario_artista):
	cur = conn.cursor()
	for user in range(0,num_usuario):
		consulta = str("select a.num as num_artista, l.nota as nota from like_artista l, num_usuario u, num_artista a where u.num = user and u.login = l.login and l.id = a.id;")
		consulta = consulta.replace("user", str(user))
		cur.execute(consulta)
		notas = cur.fetchall()
		for i in notas:
			usuario_artista[user][i[0]] = i[1]
	cur.close()
	return usuario_artista;

#Preenche a matriz com os dados necessários.
def preencheMatrizUsuariosxFilmes(conn, num_usuario, usuario_filme):
	cur = conn.cursor()
	for usuario in range(0,num_usuario):
		consulta = "SELECT A.Num AS Num_Filme, L.Nota AS Nota FROM like_filmes L, num_filmes A, num_usuario U WHERE U.Num = user AND U.login = L.login AND L.id = A.id; "
		consulta = consulta.replace("user",str(usuario))
		cur.execute(consulta)
		notas = cur.fetchall()
		for j in notas:
			usuario_filme[usuario][j[0]] = j[1]
	cur.close()
	return usuario_filme;

#Preenche a matriz com os dados de similaridade a cada dupla de usuários.
#similaridade de (A,B) e (B,A) são iguais.
#similaridade de (A,A) é 100% (1). E distância 0.
def preencheMatrizUsuariosxUsuarios(conn, num_usuario, num_filmes, usuario_usuario, usuario_filmes):
	cur = conn.cursor()
	for userA in range(0,num_usuario):
		for userB in range(0,num_usuario):
			usuario_usuario[userA][userB] = similaridade(userA,userB,usuario_filmes,num_filmes)
	return usuario_usuario;

def similaridade(usuarioA,usuarioB,usuario_filmes,num_filmes):
	#UsuarioA e UsuarioB são os números dos usuários que se quer achar a similaridade.
	#Usuario_filmes é a matriz preenchida de Usuários x Filmes
	comum = 0
	userA = set()
	userB = set()
	for filme in range(0, num_filmes):
		print("Iteração" + str(filme))
		if (usuario_filmes[usuarioA][filme] == usuario_filmes[usuarioB][filme] and usuario_filmes[usuarioA][filme]!=0):
			comum += 1
			print(comum)
		if usuario_filmes[usuarioA][filme]!=0 and usuario_filmes[usuarioB][filme]!=0:
			print(filme)
			userA.add(filme)
			userB.add(filme)
			print(userA)
			print(userB)
	total = len(userA | userB)
	if total == 0:
		return 0;
	elif():
		similaridade = comum/total
		return similaridade;

#---------------------------------
#Inicio do programa. Now the animal catches.

#Criação das Views no Banco de Dados
criaViewNumUsuario(conn)
criaViewNumFilmes(conn)
criaViewNumArtista(conn)

#Criação das matrizes e seus parametros
matriz_usuarios_filmes = criaMatrizUsuariosxFilmes(conn)
matriz_usuarios_artistas = criaMatrizUsuarioArtista(conn)
matriz_usuarios_usuarios = criaMatrizUsuarioxUsuario(conn)
numero_filmes = encontraNumeroFilmes(conn)
numero_usuarios = obtemNumeroDeUsuarios(conn)
numero_artistas = obtemNumeroDeArtistas(conn)

#Preenche as matrizes com seus dados
matriz_usuarios_filmes = preencheMatrizUsuariosxFilmes(conn,numero_usuarios,matriz_usuarios_filmes)
matriz_usuarios_artistas = preencheMatrizUsuarioArtista(conn,numero_usuarios,matriz_usuarios_artistas)

#Busca similaridade de todos com todos e preenche na matriz Usuario x Usuario.
matriz_usuarios_usuarios = preencheMatrizUsuariosxUsuarios(conn,numero_usuarios,numero_filmes,matriz_usuarios_usuarios,matriz_usuarios_filmes)
