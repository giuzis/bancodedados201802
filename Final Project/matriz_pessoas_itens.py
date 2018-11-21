import psycopg2;
import numpy as np;

#Conecta ao banco de dados
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

#Obtem o numero de artistas para a criacao da matriz
def obtemNumeroDeArtistas(conn):
	cur = conn.cursor()
	consulta = str("select count(*) from artista_musical;")
	cur.execute(consulta)
	num_artista = cur.fetchone()
	cur.close()
	return num_artista[0];

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
