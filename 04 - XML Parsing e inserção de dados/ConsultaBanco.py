import psycopg2
import psycopg2.extras
# Try to connect
try:
 conn = psycopg2.connect("dbname='1802BandoDeDados' user='<usuario>' host='200.134.10.32' password='803322'")
except:
 print "I am unable to connect to the database."

cur = conn.cursor()
try:
 cur.execute("""CREATE TABLE TESTE
 (ID INT PRIMARY KEY NOT NULL,
 NOME TEXT NOT NULL);""")
except Exception as e:
 print "I can't create table!"
 print e
conn.commit()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
 cur.execute("""SELECT * FROM taxi;""")
except Exception as e:
 print "I can't SELECT from taxi"
 print e
rows = cur.fetchall()
print "\nContents of Table Taxi:\n"
for row in rows:
 print "Placa: ", row['placa'], " -- Modelo: ", row['modelo'], " -- Ano de Fabricacao: ", row['anofab'] 