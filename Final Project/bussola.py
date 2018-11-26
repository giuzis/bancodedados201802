import psycopg2
import numpy as np
import matplotlib.pyplot as plt

try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

cur = conn.cursor()
cur2 = conn.cursor()

x = []
y = []
i = 0

try:
	cur.execute("SELECT login FROM pessoa;")
	for login in cur:
		x.append(0)
		y.append(0)
		try:
			cur2.execute("SELECT artista_musical.genero_musical, like_artista.nota FROM artista_musical, like_artista WHERE artista_musical.id = like_artista.id AND like_artista.login = '" + login[0] + "';")
			for info in cur2:
				if info[0] == 'Heavy metal music':
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
				if info[0] == 'Pop music':
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
				if info[0] == 'Alternative rock':
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
				if info[0] == 'Hip hop music':
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
ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect('equal')
ax.axhline(y=0, color='#808080')
ax.axvline(x=0, color='#808080')
ax.plot(x, y, 'ro', color='#000000')
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.fill_between([-6, 0],-6, 0,alpha=0.6, color='#00FF00')
ax.fill_between([0, 6], -6, 0, alpha=0.6, color='#F9D307')
ax.fill_between([-6, 0], 0, 6, alpha=0.6, color='#FF0000')
ax.fill_between([0, 6], 0, 6, alpha=0.6, color='#0000FF')
ax.grid(True, which='both')
text1 = ax.annotate("METAL", xy=(-1, 6), xytext=(-1, 6.2))
text2 = ax.annotate("POP", xy=(-0.5, -6), xytext=(-0.5, -6.5))
text3 = ax.annotate("ROCK", xy=(-6, -0.2), xytext=(-7.5, -0.2))
text4 = ax.annotate("HIP HOP", xy=(6, -0.2), xytext=(6.2, -0.2))
pos = 0
listax = []
listay = []
while pos <= 45:
	flag = 0
	if pos > 0:
		i = 0
		for coisa in listax:
			if(x[pos] == coisa and y[pos] == listay[i]):
				flag = 1
				break
			i += 1
	if(flag == 0):
		ax.text(x[pos] - 0.2, y[pos] + 0.25, str(pos + 1), fontsize=6)
	listax.append(x[pos])
	listay.append(y[pos])
	pos += 1
plt.show()