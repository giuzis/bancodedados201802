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
#Cria o Hypercubo Usuario x Usuario x Conjunto.
def criaHypercuboUsuarioxUsuario(conn):
	num_usuario = obtemNumeroDeUsuarios(conn)
	usuario_usuario = np.zeros((num_usuario,num_usuario,3))
	#Na terceira* dimensão, tem-se:
	#[0], similaridade
	#[1], set(A)
	#[2], set(B)
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
def preencheHypercuboUsuariosxUsuarios(conn, num_usuario, num_filmes, usuario_usuario, usuario_filmes):
	cur = conn.cursor()
	for userA in range(0,num_usuario):
		for userB in range(0,num_usuario):
			usuario_usuario = similaridade(userA,userB,usuario_filmes,num_filmes,num_usuario,usuario_usuario)
			#usuario_usuario[userA][userB][0] = similaridade(userA,userB,usuario_filmes,num_filmes)
	return usuario_usuario;

def similaridade(usuarioA,usuarioB,usuario_filmes,num_filmes,num_usuario,usuario_usuario):
	#UsuarioA e UsuarioB são os números dos usuários que se quer achar a similaridade.
	#Usuario_filmes é a matriz preenchida de Usuários x Filmes
	userA = set()
	userB = set()
	usuario_usuario[usuarioA][usuarioB][1] = userA
	usuario_usuario[usuarioA][usuarioB][2] = set()
	for filme in range(0, num_filmes):
		#Parte 1 - Calcula Filmes em comum entre A e B.
		if((usuario_filmes[usuarioA][filme] == usuario_filmes[usuarioB][filme]) and (usuario_filmes[usuarioA][filme]!=0 or usuario_filmes[usuarioB][filme]!=0)):
			#Os dois dão a mesma nota, e a nota não é zero.
			usuario_usuario[usuarioA][usuarioB][1].add(filme)
			usuario_usuario[usuarioA][usuarioB][2].add(filme)
		elif(usuario_filmes[usuarioA][filme]!=usuario_filmes[usuarioB][filme] and usuario_filmes[usuarioA][filme]!=0):
			#São notas diferentes. Preenche em A os filmes que não forem 0.
			usuario_usuario[usuarioA][usuarioB][1].add(filme)
		elif(usuario_filmes[usuarioA][filme]!=usuario_filmes[usuarioB][filme] and usuario_filmes[usuarioB][filme]!=0):
			#São notas diferentes. Preenche em B os filmes que não forem 0.
			usuario_usuario[usuarioA][usuarioB][2].add(filme)
	distância = distanciaJaccard(usuario_usuario[usuarioA][usuarioB][1],usuario_usuario[usuarioA][usuarioB][2])
	return usuario_usuario;
"""
		#Preenche filmes diferentes de 0 para o usuario A no set de A.
		if(usuario_filmes[usuarioA][filme]!=0):
			userA.add(filme)
			#Preenche o set de A para todas as pessoas.
			#Seria melhor com ponteiro eu diria.
			for j in range(0,num_usuario)
			usuario_usuario[usuarioA][j][1].add(filme)

		#Preenche filmes diferentes de 0 para o usuario B no set de B.
		if(usuario_filmes[usuarioB][filme][0]!=0):
			usuario_filmes[usuarioB][filme][1]
			userB.add(filme)
		if ((usuario_filmes[usuarioA][filme] == usuario_filmes[usuarioB][filme]) and (usuario_filmes[usuarioA][filme]!=0 or usuario_filmes[usuarioB][filme]!=0)):
			userA.add(filme)
			userB.add(filme)
		if (usuario_filmes[usuarioA][filme]!=0) or usuario_filmes[usuarioB][filme]!=0):
			userA.add(filme)
			userB.add(filme)
				total = len(userA | userB)
	if total == 0:
		return 0;
	similaridade = comum/total
	return similaridade;
	União dos conjuntos de filmes de A e de B.
"""
#Função para padronizar as notas de 0 a 5 para 0, 1 ou 2.
def padronizacao(dimensao1,dimensao2,matriz):
	matriz_padronizada = np.zeros((dimensao1,dimensao2))
	for i in range(0,dimensao1):
		for j in range(0,dimensao2):
			if matriz[i][j] == 5 or matriz[i][j] == 4:
				matriz_padronizada[i][j] = 2
				#Se a nota for 5 ou 4, recebe nota máxima padronizada, ou seja, 2.
			elif matriz[i][j] == 3 or matriz[i][j] == 2 or matriz[i][j] == 1:
				matriz_padronizada[i][j] = 1
	return matriz_padronizada;


#Função para buscar informações de um par de usuários A,B
def buscaSimilaridadeUsuarioxUsuario(usuarioA,usuarioB,matriz_usuarios_usuarios,conn):
	cur = conn.cursor();
	consultaA = "SELECT P.nome_completo FROM Pessoa P, num_usuario N WHERE N.num = userA AND P.login = N.login"
	consultaB = "SELECT P.nome_completo FROM Pessoa P, num_usuario N WHERE N.num = userB AND P.login = N.login"
	consultaA = consultaA.replace("userA",str(usuarioA))
	consultaB = consultaB.replace("userB",str(usuarioB))
	cur.execute(consultaA)
	nome_usuarioA = cur.fetchall()
	cur.close()
	cur = conn.cursor()
	cur.execute(consultaB)
	nome_usuarioB = cur.fetchall()
	#print(usuarioA,nome_usuarioA,usuarioB,nome_usuarioB)
	similaridade = float(matriz_usuarios_usuarios[int(usuarioA)][int(usuarioB)])*100
	similaridade = round(similaridade,3)
	"""print(matriz_usuarios_usuarios[int(usuarioA)][int(usuarioB)])
	print(int(usuarioB))
	print(similaridade)
	print(usuarioA,usuarioB)"""
	if usuarioA==usuarioB:
		return print("São a mesma pessoa, similaridade é: 100%");
	if usuarioA!=usuarioB:
			return print("\nA similaridade entre " + str(nome_usuarioA) + " e entre " + str(nome_usuarioB) + " é de " + str(similaridade) + "%.\n");
#round(number,places)

#---------------------------------
#Inicio do programa. Now the animal catches.

#Criação das Views no Banco de Dados
criaViewNumUsuario(conn)
criaViewNumFilmes(conn)
criaViewNumArtista(conn)

#Criação das matrizes e seus parametros
matriz_usuarios_filmes = criaMatrizUsuariosxFilmes(conn)
matriz_usuarios_artistas = criaMatrizUsuarioArtista(conn)
matriz_usuarios_usuarios = criaHypercuboUsuarioxUsuario(conn)
numero_filmes = encontraNumeroFilmes(conn)
numero_usuarios = obtemNumeroDeUsuarios(conn)
numero_artistas = obtemNumeroDeArtistas(conn)

#Preenche as matrizes com seus dados
matriz_usuarios_filmes = preencheMatrizUsuariosxFilmes(conn,numero_usuarios,matriz_usuarios_filmes)
matriz_usuarios_artistas = preencheMatrizUsuarioArtista(conn,numero_usuarios,matriz_usuarios_artistas)

#Padroniza as matrizes para o padrão de notas [0 a 5] para [0 a 2]
matriz_usuarios_filmes = padronizacao(numero_usuarios,numero_filmes,matriz_usuarios_filmes)


#Busca similaridade de todos com todos e preenche na matriz Usuario x Usuario.
matriz_usuarios_usuarios = preencheHypercuboUsuariosxUsuarios(conn,numero_usuarios,numero_filmes,matriz_usuarios_usuarios,matriz_usuarios_filmes)

#Little Menu for Searching similarity among two users.
"""for i in range(0,numero_filmes):
	print("Filme nº: " + str(i))
	print(matriz_usuarios_filmes[10][i])
	print(matriz_usuarios_filmes[4][i])
	print(matriz_usuarios_usuarios[10][4])"""

menu_on = True;
print("Bem vindo ao menu de busca por similaridade! Digite o número da opção que queira utilizar: ")
while(menu_on):
	print("1 - Buscar similaridade entre dois usuários \n(OBS: Atualmente, apenas leva em consideração os filmes em comum.")
	print("2 - Sair do programa.")
	option = input("Digite a opção desejada: ")
	if option == "1":
		print("Digite os números dos usuários que queria saber o grau de similaridade. \nAtualmente, esta similaridade está baseada nos filmes em que ambos os usuários curtiram ou não! ")
		userA = input("Digite o número do usuário 1: ")
		userB = input("Digite o número do usuario 2: ")
		buscaSimilaridadeUsuarioxUsuario(userA,userB,matriz_usuarios_usuarios,conn);
		#print("Agora estou com preguiça de continuar funcionando. \n Contate o desenvolvedor para maiores informações. \n Desligando... ")
		#menu_on = False;
	if option == "2":
		print("Saindo...")
		menu_on = False;
print("Obrigado por utilizar o nosso sistema! Volte Sempre!")

