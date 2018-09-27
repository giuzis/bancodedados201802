--Olá pessoal! Adicionem aqui as querys SQL que serão usadas na resposta do trabalho 07 de BD!
--Qual é a média e desvio padrão dos ratings para artistas musicais e filmes?
SELECT AVG(like_filmes.nota) AS Media, STDDEV(like_filmes.nota) AS DesvioPadrao FROM like_filmes;
--Quais são os artistas e filmes com o maior rating médio curtidos por pelo menos duas pessoas? Ordenados por rating médio.

--Quais são os 10 artistas musicais e filmes mais populares? Ordenados por popularidade.

--Crie uma view chamada ConheceNormalizada que represente simetricamente os relacionamentos de conhecidos da turma. Por exemplo, se a conhece b mas b não declarou conhecer a, a view criada deve conter o relacionamento (b,a) além de (a,b).

--Quais são os conhecidos (duas pessoas ligadas na view ConheceNormalizada) que compartilham o maior numero de filmes curtidos?

--Qual o número de conhecidos dos conhecidos (usando ConheceNormalizada) para cada integrante do seu grupo?

--Construa um gráfico para a função f(x) = (número de pessoas que curtiram exatamente x filmes).

--Construa um gráfico para a função f(x) = (número de filmes curtidos por exatamente x pessoas).

--Defina duas outras informações (como as anteriores) que seriam úteis para compreender melhor a rede. Agregue estas informações à sua aplicação.