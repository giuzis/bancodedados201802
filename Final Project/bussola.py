import psycopg2
import numpy as np
import matplotlib.pyplot as plt

try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

cur = conn.cursor()
cur2 = conn.cursor()

generosmetal = []
generospop = []
generosrock = []
generoshiphop = []
x = []
y = []
i = 0

try:
	cur.execute("SELECT * FROM metal;")
	for genero in cur:
		generosmetal.append(genero[0])
except Exception as e:
	print(e)

try:
	cur.execute("SELECT * FROM pop;")
	for genero in cur:
		generospop.append(genero[0])
except Exception as e:
	print(e)

try:
	cur.execute("SELECT * FROM rock;")
	for genero in cur:
		generosrock.append(genero[0])
except Exception as e:
	print(e)

try:
	cur.execute("SELECT * FROM hip_hop;")
	for genero in cur:
		generoshiphop.append(genero[0])
except Exception as e:
	print(e)

try:
	cur.execute("SELECT login FROM pessoa;")
	for login in cur:
		x.append(0)
		y.append(0)
		try:
			cur2.execute("SELECT artista_musical.genero_musical, like_artista.nota FROM artista_musical, like_artista WHERE artista_musical.id = like_artista.id AND like_artista.login = '" + login[0] + "';")
			for info in cur2:
				for metal in generosmetal:
					if info[0] == metal:
						if info[1] == 1:
							y[i] -= 2
						if info[1] == 2:
							y[i] -= 1
						if info[1] == 3:
							y[i] += 0
						if info[1] == 4:
							y[i] += 1
						if info[1] == 5:
							y[i] += 2 
					else:
						pass
				for pop in generospop:
					if info[0] == pop:
						if info[1] == 1:
							y[i] += 2
						if info[1] == 2:
							y[i] += 1
						if info[1] == 3:
							y[i] -= 0
						if info[1] == 4:
							y[i] -= 1
						if info[1] == 5:
							y[i] -= 2 
					else:
						pass
				for rock in generosrock:
					if info[0] == rock:
						if info[1] == 1:
							x[i] += 2
						if info[1] == 2:
							x[i] += 1
						if info[1] == 3:
							x[i] -= 0
						if info[1] == 4:
							x[i] -= 1
						if info[1] == 5:
							x[i] -= 2 
					else:
						pass
				for hiphop in generoshiphop:
					if info[0] == hiphop:
						if info[1] == 1:
							x[i] -= 2
						if info[1] == 2:
							x[i] -= 1
						if info[1] == 3:
							x[i] += 0
						if info[1] == 4:
							x[i] += 1
						if info[1] == 5:
							x[i] += 2 
					else:
						pass
			i += 1
		except Exception as e:
			print(e)
except Exception as e:
	print(e)

posy = 0
for coisa in x: 
	print("(" + str(coisa) + ", " + str(y[posy]) + ")")
	posy += 1

fig, ax = plt.subplots()
ax.set_xlim(-13,13)
ax.set_ylim(-13,13)
ax.set_aspect('equal')
ax.axhline(y=0, color='#808080')
ax.axvline(x=0, color='#808080')
ax.plot(x, y, 'ro', color='#000000')
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.fill_between([-13, 0],-13, 0,alpha=0.6, color='#00FF00')
ax.fill_between([0, 13], -13, 0, alpha=0.6, color='#F9D307')
ax.fill_between([-13, 0], 0, 13, alpha=0.6, color='#FF0000')
ax.fill_between([0, 13], 0, 13, alpha=0.6, color='#0000FF')
ax.grid(True, which='both')
text1 = ax.annotate("METAL", xy=(-1, 13), xytext=(-1, 13.2))
text2 = ax.annotate("POP", xy=(-0.5, -13), xytext=(-0.9, -14))
text3 = ax.annotate("ROCK", xy=(-13, -0.2), xytext=(-16, -0.2))
text4 = ax.annotate("HIP HOP", xy=(13, -0.2), xytext=(13.2, -0.2))
plt.show()

