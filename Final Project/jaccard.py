def distanciaJaccard(conjuntoA,conjuntoB):
    conjuntoA = set(conjuntoA.split())
    conjuntoB = set(conjuntoB.split())
    #Set.split apenas separa os elementos do set de maneira individual.
    coeficiente = float(len(conjuntoA & conjuntoB) / len(conjuntoA | conjuntoB))
    return 1 - coeficiente

#Exemplos Teste
#---------------------------------
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


