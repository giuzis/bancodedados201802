--Olá pessoal! Adicionem aqui as querys SQL que serão usadas na resposta do trabalho 07 de BD!

--Qual é a média e desvio padrão dos ratings para artistas musicais e filmes?
SELECT  ROUND(AVG(like_filmes.nota),3) AS Media, ROUND(STDDEV(like_filmes.nota),3) AS DesvioPadrao FROM like_filmes;
SELECT ROUND(AVG(like_artista.nota),3) AS Media, ROUND(STDDEV(like_artista.nota),3) AS DesvioPadrao FROM like_artista;

--Quais são os artistas e filmes com o maior rating médio curtidos por pelo menos duas pessoas? Ordenados por rating médio.
--Artistas
CREATE VIEW artistas_por_like AS SELECT  artista_musical.nome_artistico,  artista_musical.id, COUNT(artista_musical.nome_artistico) AS num_curtidas FROM artista_musical, like_artista WHERE artista_musical.id = like_artista.id GROUP BY artista_musical.nome_artistico, artista_musical.id ORDER BY artista_musical.nome_artistico;
SELECT ROUND(AVG(like_artista.nota),3) AS Media, artistas_por_like.nome_artistico FROM like_artista, artistas_por_like WHERE  like_artista.id = artistas_por_like.id AND artistas_por_like.num_curtidas >= 2 GROUP BY artistas_por_like.nome_artistico ORDER BY media DESC;
--Filmes
CREATE VIEW filmes_por_like AS SELECT  filmes.id, COUNT(filmes.id) AS num_curtidas FROM filmes, like_filmes WHERE filmes.id = like_filmes.id GROUP BY  filmes.id;
SELECT ROUND(AVG(like_filmes.nota),3) AS Media, filmes_por_like.id FROM like_filmes, filmes_por_like WHERE like_filmes.id = filmes_por_like.id AND filmes_por_like.num_curtidas >=2 GROUP BY filmes_por_like.id ORDER BY media DESC;


--Quais são os 10 artistas musicais e filmes mais populares? Ordenados por popularidade.
SELECT ROUND(AVG(like_filmes.nota),3) AS Media, filmes_por_like.id FROM like_filmes, filmes_por_like WHERE like_filmes.id = filmes_por_like.id AND filmes_por_like.num_curtidas >=2 GROUP BY (filmes_por_like.id)  ORDER BY media DESC LIMIT 10;
SELECT ROUND(AVG(like_artista.nota),3) AS Media, artistas_por_like.nome_artistico FROM like_artista, artistas_por_like WHERE  like_artista.id = artistas_por_like.id AND artistas_por_like.num_curtidas >= 2 GROUP BY artistas_por_like.nome_artistico ORDER BY Media DESC LIMIT 10;

--Crie uma view chamada ConheceNormalizada que represente simetricamente os relacionamentos de conhecidos da turma. Por exemplo, se a conhece b mas b não declarou conhecer a, a view criada deve conter o relacionamento (b,a) além de (a,b).

--Quais são os conhecidos (duas pessoas ligadas na view ConheceNormalizada) que compartilham o maior numero de filmes curtidos?

--Qual o número de conhecidos dos conhecidos (usando ConheceNormalizada) para cada integrante do seu grupo?

--Construa um gráfico para a função f(x) = (número de pessoas que curtiram exatamente x filmes).
--CREATE VIEW num AS SELECT COUNT(like_filmes.login) FROM like_filmes GROUP BY like_filmes.login;
--SELECT count, count(*) AS quantpessoas FROM num GROUP BY count;
--Construa um gráfico para a função f(x) = (número de filmes curtidos por exatamente x pessoas).
--CREATE VIEW num2 AS SELECT COUNT(like_filmes.id) FROM like_filmes GROUP BY like_filmes.id;
--SELECT count, count(*) AS numpessoas FROM num2 GROUP BY count ORDER BY count;
--Defina duas outras informações (como as anteriores) que seriam úteis para compreender melhor a rede. Agregue estas informações à sua aplicação.
