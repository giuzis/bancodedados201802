import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from itertools import groupby

try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print("Falha ao se conectar ao banco de dados.")

cur = conn.cursor()
cur2 = conn.cursor()

x = []
y = []
logins = []
i = 0

try:
	cur.execute("SELECT login FROM pessoa;")
	for login in cur:
		logins.append(login[0])
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

loginsgrupos = []
fig, ax = plt.subplots()
ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect('equal')
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
num = 0
listax = []
listay = []
while pos <= 45:
	flag = 0
	if pos > 0:
		i = 0
		for coisa in listax:
			if(x[pos] == listax[i] and y[pos] == listay[i]):
				flag = 1
				break
			i += 1
	if(flag == 0):
		ax.text(x[pos] - 0.2, y[pos] + 0.25, str(num + 1), fontsize=6)
		listax.append(x[pos])
		listay.append(y[pos])
		loginsgrupos.append(logins[pos])
		num += 1
	pos += 1

X = np.column_stack((listax, listay))

Pessoas1 = np.column_stack((x, y, logins))
print(Pessoas1)

Pessoas = np.column_stack((listax, listay, loginsgrupos))
print(Pessoas)

kmeans = KMeans(n_clusters=4, random_state=0).fit(X)

grupo1 = []
grupo2 = []
grupo3 = []
grupo4 = []
fig, ax2 = plt.subplots()
ax2.set_xlim(-6,6)
ax2.set_ylim(-6,6)
ax2.set_aspect('equal')
ax2.set_yticklabels([])
ax2.set_xticklabels([])
i = 0
for indice in kmeans.labels_:
	if indice == 0:
		ax2.plot(listax[i], listay[i], 'ro', color='#0000FF')
		grupo1.append(Pessoas[i][2])
	if indice == 1:
		ax2.plot(listax[i], listay[i], 'ro', color='#FF0000')
		grupo2.append(Pessoas[i][2])
	if indice == 2:
		ax2.plot(listax[i], listay[i], 'ro', color='#F9D307')
		grupo3.append(Pessoas[i][2])
	if indice == 3:
		ax2.plot(listax[i], listay[i], 'ro', color='#00FF00')
		grupo4.append(Pessoas[i][2])
	i += 1
ax2.grid(True, which='both')

nomesgrupo1 = []
nomesgrupo2 = []
nomesgrupo3 = []
nomesgrupo4 = []
for nome1 in grupo1:
	cur.execute("SELECT nome_completo FROM pessoa WHERE login = '" + nome1 +"'")
	for nome in cur:
		nomesgrupo1.append(nome[0])
for nome2 in grupo2:
	cur.execute("SELECT nome_completo FROM pessoa WHERE login = '" + nome2 +"'")
	for nome in cur:
		nomesgrupo2.append(nome[0])
for nome3 in grupo3:
	cur.execute("SELECT nome_completo FROM pessoa WHERE login = '" + nome3 +"'")
	for nome in cur:
		nomesgrupo3.append(nome[0])
for nome4 in grupo4:
	cur.execute("SELECT nome_completo FROM pessoa WHERE login = '" + nome4 +"'")
	for nome in cur:
		nomesgrupo4.append(nome[0])

print("Grupo 1:")
print(nomesgrupo1)
print("Grupo 2:")
print(nomesgrupo2)
print("Grupo 3:")
print(nomesgrupo3)
print("Grupo 4:")
print(nomesgrupo4)

plt.show()