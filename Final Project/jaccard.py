#Biblioteca para acesso ao Banco de Dados
import pyscopg2;
#Biblioteca Matematica
import numpy as numpy;


#------------------------------
#Funçoes utilizadas nesse programa

#Encontra a distancia de Jaccard dado conjunto A e B.
def distanciaJaccard(conjuntoA,conjuntoB):
    conjuntoA = set(conjuntoA.split())
    conjuntoB = set(conjuntoB.split())
    #Set.split apenas separa os elementos do set de maneira individual.
    coeficiente = float(len(conjuntoA & conjuntoB) / len(conjuntoA | conjuntoB))
    return 1 - coeficiente

#Exemplos Teste
#---------------------------------
def JaccardTest():
	A = '1 2 3 4 5 6 7 8 9 10'
	B = '1 2 3 4 5 6 7 8 9 10'
	C = '2 3 4 5 6 7 8 9 10 11'
	D = '10 11 12 13 14 15 16 17'
	print(distanciaJaccard(A,B))
	print(distanciaJaccard(A,C))
	print(distanciaJaccard(A,D))
	print(distanciaJaccard(C,D))
#---------------------------------
#Imaginando que os conjuntos sejam generos musicais.
#A é Rock e seus elementos são músicas de Rock.
#A distância é medida entre conjuntos, então é preciso transformar
#temporariamente, cada pessoa como um conjunto, e seus atributos são suas músicas.
#A distância pede o quanto ela está de cada polo musical, indicando sua posição
#Na bússola musicista.

#Encontra o número de filmes para criação da Matriz
def encontraNumeroFilmes(conn):
	cur = conn.cursor()
	consulta = "SELECT count(*) FROM Filmes;"
	cur.execute(consulta)
	num_filmes = cur.fetchone()
	cur.close()
	return num_filmes[0];

#Obtem o numero de usuarios para a criacao da matriz
#É a mesma função da Giu.
def obtemNumeroDeUsuarios(conn):
	cur = conn.cursor()
	consulta = "SELECT count(*) FROM Pessoa;"
	cur.execute(consulta)
	num_usuario = cur.fetchone()
	cur.close()
	return num_usuario[0];

#Cria a Matriz UsuariosxFilmes.
def criaMatrizUsuariosxFilmes(conn):
	num_usuario = obtemNumeroDeUsuarios(conn)
	num_filmes = encontraNumeroFilmes(conn)
	usuario_filme = numpy.zeros((num_usuario,num_filmes))
	return usuario_filme;

#Preenche a matriz com os dados necessários.
def preencheMatrizUsuariosxFilmes(conn, num_usuario, usuario_filme):
	cur = conn.cursor()
	for usuario in range(0,num_usuario):
		consulta = "SELECT "





#---------------------------------
#Inicio do programa.
try:
	connection = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

