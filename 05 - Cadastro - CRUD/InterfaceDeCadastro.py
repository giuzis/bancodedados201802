import psycopg2
import psycopg2.extras
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def delete(NomePessoa):
	try:
 		conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
	except:
 		print "I am unable to connect to the database."

	cur = conn.cursor()

	try:
 		cur.execute("DELETE FROM pessoa WHERE pessoa.nome LIKE '" + NomePessoa + "';")
	except Exception as e:
 		print "Nao foi possivel apagar"
		print e
 	conn.commit()
 	cur.close()
 	conn.close()

def listagem():
	try:
	 	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
	except:
	 	print "I am unable to connect to the database."

	conn.set_client_encoding('LATIN9')
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM pessoa;")
		for pessoas in cur:
			print(unicode(unicode(pessoas[0]) + ", " + unicode(pessoas[1]) + ", " + unicode(pessoas[2]) + ", " + unicode(pessoas[3])))
	except Exception as e:
	 	print "Nao foi possivel inserir"
	 	print e
	conn.commit()
	cur.close()
	conn.close()

print("//////////////MENU///////////////") 
menu = raw_input("Aperte 1 para listar as pessoas\n")
if menu == "1":
	listagem();
