	CREATE table Pessoa
	(
		Login VARCHAR(15) NOT NULL,
		Nome_Completo VARCHAR(100) NOT NULL,
		Cidade_Natal VARCHAR(50),
		Data_Nascimento	DATE,
		PRIMARY KEY (Login) 
	);

	CREATE TABLE Bloqueia 
	(
		Login1 VARCHAR(15) NOT NULL,
		Login2 VARCHAR(15) NOT NULL,
		Motivo VARCHAR(255),
		PRIMARY KEY (Login1, Login2),
		FOREIGN KEY(Login1) REFERENCES Pessoa(Login)
		    ON DELETE   NO ACTION
		    ON UPDATE   NO ACTION,
		FOREIGN KEY(Login2) REFERENCES Pessoa(Login)
		    ON DELETE   NO ACTION
		    ON UPDATE   NO ACTION
	);
	
	CREATE TABLE Conhece
	(
	    Login1 VARCHAR(15) NOT NULL,
	    Login2 VARCHAR(15) NOT NULL,
	    PRIMARY KEY (Login1, Login2),
	    FOREIGN KEY(Login1) REFERENCES Pessoa(login)
		    ON DELETE   NO ACTION
		    ON UPDATE   NO ACTION,
		FOREIGN KEY(Login2) REFERENCES Pessoa(login)
		    ON DELETE   NO ACTION
		    ON UPDATE   NO ACTION
	);
	
	CREATE TABLE Categoria
	(
	    Nome VARCHAR(55) NOT NULL,
	    Categoria VARCHAR(55),
	    PRIMARY KEY (Nome),
	    FOREIGN KEY (Categoria) REFERENCES Categoria(Nome)
	        ON DELETE NO ACTION 
	        ON UPDATE NO ACTION
	);
	
	CREATE TABLE Filmes
	(
	    ID INTEGER NOT NULL,
	    Nome VARCHAR(55) NOT NULL,
	    Data_de_Lançamento DATE,
	    Categoria VARCHAR(55),
	    PRIMARY KEY (ID),
	    FOREIGN KEY (Categoria) REFERENCES Categoria(Nome)
		    ON DELETE   NO ACTION
		    ON UPDATE   NO ACTION
	);
	
	CREATE TABLE Like_Filmes
	(
	    Login VARCHAR(15) NOT NULL,
	    ID INTEGER NOT NULL,
	    Nota INTEGER,
	    PRIMARY KEY (Login, ID),
	    FOREIGN KEY (ID) REFERENCES Filmes(ID)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION,
	   FOREIGN KEY (Login) REFERENCES Pessoa(Login)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION
	);
	
	CREATE TABLE Artista_Musical
	(
		ID INTEGER NOT NULL,
		Genero_Musical VARCHAR(50) NOT NULL,
		Nome_Artistico VARCHAR(55) NOT NULL,
		Pais VARCHAR(50) NOT NULL,
		PRIMARY KEY (ID)
	);
	
	CREATE TABLE Like_Artista
	(
	    Login VARCHAR(15) NOT NULL,
	    ID INTEGER NOT NULL,
	    Nota INTEGER NOT NULL,
	    PRIMARY KEY (Login, ID)
	    FOREIGN KEY (Login) REFERENCES Pessoa(Login)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION
	);
	
	CREATE TABLE Cantor
	(
	    ID INTEGER NOT NULL,
	    PRIMARY KEY (ID),
	    FOREIGN KEY (ID) REFERENCES Artista_Musical (ID)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION
	);
	
	CREATE TABLE Banda
	(
	    ID INTEGER NOT NULL,
	    PRIMARY KEY (ID),
	    FOREIGN KEY (ID) REFERENCES Artista_Musical (ID)
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION
	);
	
	CREATE TABLE Musico
	(
	    Nome_Real VARCHAR(55) NOT NULL,
	    Estilo_Musical VARCHAR(55) NOT NULL,
	    Data_Nascimento DATE NOT NULL,
	    IDCantor INTEGER NOT NULL,
	    IDBanda INTEGER NOT NULL,
	    FOREIGN KEY (IDCantor) REFERENCES Cantor(ID) NULL
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION,
	    FOREIGN KEY (IDBanda) REFERENCES Banda(ID) NULL
	        ON DELETE NO ACTION
	        ON UPDATE NO ACTION
	);
	
		CREATE TABLE Membros
	(
	    ID INTEGER NOT NULL,
	    TELEFONE INTEGER,
	    ENDERECO VARCHAR(50),
	    PRIMARY KEY (ID)
	);
	
	CREATE TABLE Atores
	(
	    ID INTEGER NOT NULL,
	    TELEFONE INTEGER,
	    ENDERECO VARCHAR(50),
	    PRIMARY KEY (ID),
	    FOREIGN KEY (ID) REFERENCES Membros(ID)
	);
	
	CREATE TABLE Diretor
	(
	    ID INTEGER NOT NULL,
	    TELEFONE INTEGER,
	    ENDERECO VARCHAR(50),
	    PRIMARY KEY (ID),
	    FOREIGN KEY (ID) REFERENCES Membros(ID)
	);


    CREATE TABLE Atua_Filmes
    (
        ID_Ator INTEGER NOT NULL,
        ID_Filmes INTEGER NOT NULL,
        PRIMARY KEY (ID_Ator, ID_Filmes),
        FOREIGN KEY (ID_Ator) REFERENCES Atores(ID),
        FOREIGN KEY (ID_Filmes) REFERENCES Filmes(ID)
    );
    
    CREATE TABLE Dirige_Filmes
    (
        ID_Diretor INTEGER NOT NULL,
        ID_Filmes INTEGER NOT NULL,
        PRIMARY KEY (ID_Diretor, ID_Filmes),
        FOREIGN KEY (ID_Diretor) REFERENCES Diretor(ID),
        FOREIGN KEY (ID_Filmes) REFERENCES Filmes(ID)
    );

    INSERT INTO pessoa VALUES
    (
		'asdrubal36',
		'Asdrubal Borba',
		'Querência do Norte',
		'1987-02-15'
    );

   	INSERT INTO pessoa VALUES
    (
		'quincas67',
		'Quincas Borba',
		'Querência do Norte',
		'1989-06-22'
    );

    INSERT INTO pessoa VALUES
    (
		'alcebiadesvn',
		'Alcebiades Venério',
		'Matelândia',
		'1995-03-03'
    );

    INSERT INTO bloqueia VALUES
    (
		'alcebiadesvn',
		'quincas67',
		'Spam'
    );

    INSERT INTO bloqueia VALUES
    (
		'alcebiadesvn',
		'asdrubal36',
		'Spam'
    );

    INSERT INTO bloqueia VALUES
    (
		'asdrubal36',
		'alcebiadesvn',
		'Comportamento toxico'
    );

    INSERT INTO bloqueia VALUES
    (
		'quincas67',
		'alcebiadesvn',
		'Atitude negativa'
    );

    INSERT INTO bloqueia VALUES
    (
		'asdrubal36',
		'quincas67',
		'Falta de carater'
    );

    INSERT INTO bloqueia VALUES
    (
		'quincas67',
		'asdrubal36',
		'Falta de educação'
    );

    INSERT INTO conhece VALUES
    (
		'quincas67',
		'asdrubal36'
	);

    INSERT INTO conhece VALUES
    (
		'quincas67',
		'alcebiadesvn'
	);

	INSERT INTO conhece VALUES
    (
		'alcebiadesvn',
		'asdrubal36'
	);

	INSERT INTO conhece VALUES
    (
		'alcebiadesvn',
		'quincas67'
	);

	INSERT INTO conhece VALUES
    (
		'asdrubal36',
		'quincas67'
	);

	INSERT INTO conhece VALUES
    (
		'asdrubal36',
		'alcebiadesvn'
	);

	INSERT INTO categoria VALUES
	(
		'Drama',
		NULL
	);

	INSERT INTO categoria VALUES
	(
		'Animação',
		NULL
	);

	INSERT INTO categoria VALUES
	(
		'Drama Policia',
		'Drama'
	);

	INSERT INTO filmes VALUES
    (
		245783,
		'O Poderoso Chefão',
		'1972-07-07',
		'Drama'
    );

    INSERT INTO filmes VALUES
    (
		543128,
		'Cinquenta Tons de Cinza',
		'2015-02-12',
		'Drama'
    );

    INSERT INTO filmes VALUES
    (
		090807,
		'Como Treinar o Seu Dragão',
		'2010-03-26',
		'Animação'
    );

    INSERT INTO like_filmes VALUES
    (
    	'quincas67',
    	245783,
    	10
    );

    INSERT INTO like_filmes VALUES
    (
    	'quincas67',
    	090807,
    	8
    );

    INSERT INTO like_filmes VALUES
    (
    	'alcebiadesvn',
    	245783,
    	2
    );

    INSERT INTO like_filmes VALUES
    (
    	'alcebiadesvn',
    	090807,
    	10
    );

    INSERT INTO like_filmes VALUES
    (
    	'asdrubal36',
    	543128,
    	10
    );

    INSERT INTO like_filmes VALUES
    (
    	'asdrubal36',
    	090807,
    	0
    );

    INSERT INTO membros VALUES
    (
    	636253,
    	999543726,
    	'Los Angeles, Califórnia, EUA'
    );

    INSERT INTO membros VALUES
    (
    	454647,
    	999120954,
    	'Lexington, Kentucky, EUA'
    );

    INSERT INTO membros VALUES
    (
    	765432,
    	999665544,
    	'Virginia, Minnesota, EUA'
    );

    INSERT INTO membros VALUES
    (
    	000001,
    	999999999,
    	'Manhattan, Nova Iorque, EUA'
    );

    INSERT INTO atores VALUES
    (
    	636253,
    	999543726,
    	'Los Angeles, Califórnia, EUA'
    );

	INSERT INTO atores VALUES
    (
    	454647,
    	999120954,
    	'Lexington, Kentucky, EUA'
    );

    INSERT INTO atores VALUES
    (
    	765432,
    	999665544,
    	'Virginia, Minnesota, EUA'
    );

    INSERT INTO diretor VALUES
    (
    	636253,
    	999543726,
    	'Los Angeles, Califórnia, EUA'
	);

	INSERT INTO diretor VALUES
    (
    	454647,
    	999120954,
    	'Lexington, Kentucky, EUA'
    );

    INSERT INTO diretor VALUES
    (
    	000001,
    	999999999,
    	'Manhattan, Nova Iorque, EUA'
    );

    INSERT INTO atua_filmes VALUES
    (
    	636253,
    	245783
    );

    INSERT INTO atua_filmes VALUES
    (
    	454647,
    	543128
    );

    INSERT INTO atua_filmes VALUES
    (
    	765432,
    	543128
    );

    INSERT INTO dirige_filmes VALUES
    (
    	636253,
    	543128
    );

    INSERT INTO dirige_filmes VALUES
    (
    	454647,
    	090807
    );

    INSERT INTO dirige_filmes VALUES
    (
    	000001,
    	090807
    );

    INSERT INTO artista_musical VALUES
    (
    	000001,
    	'Funk',
    	'Mr Catra',
    	'Brasil'
    );

    INSERT INTO artista_musical VALUES
    (
    	435261,
    	'New Metal',
    	'Linkin Park',
    	'EUA'
    );

    INSERT INTO artista_musical VALUES
    (
    	565758,
    	'Indie pop',
    	'Lorde',
    	'EUA'
    );

    INSERT INTO artista_musical VALUES
    (
    	123543,
    	'Industrial Metal',
    	'Rammstein',
    	'Alemanha'
    );

    INSERT INTO artista_musical VALUES
    (
    	4019283,
    	'Rock',
    	'Queen',
    	'Reino Unido'
    );

    INSERT INTO artista_musical VALUES
    (
    	789653,
    	'Pop',
    	'Michael Jackson',
    	'EUA'
    );

    INSERT INTO like_artista VALUES
    (
    	'quincas67',
    	000001,
    	10
    );

    INSERT INTO like_artista VALUES
    (
    	'asdrubal36',
    	000001,
    	10
    );

    INSERT INTO like_artista VALUES
    (
    	'alcebiadesvn',
    	000001,
    	10
    );

    INSERT INTO like_artista VALUES
    (
    	'quincas67',
    	435261,
    	9
    );

    INSERT INTO like_artista VALUES
    (
    	'asdrubal36',
    	565758,
    	7
    );

    INSERT INTO like_artista VALUES
    (
    	'alcebiadesvn',
    	435261,
    	2
    );

    INSERT INTO cantor VALUES
    (
    	000001
	);

	INSERT INTO cantor VALUES
    (
    	565758
	);

	INSERT INTO cantor VALUES
    (
    	789653
	);

	INSERT INTO banda VALUES
    (
    	435261
	);

	INSERT INTO banda VALUES
    (
    	123543
	);

	INSERT INTO banda VALUES
    (
    	4019283
	);

	INSERT INTO musico VALUES
	(
		'Wagner Domingues Costa',
		'Funk',
		'1968-11-05',
		000001,
		NULL
	);

	INSERT INTO musico VALUES
	(
		'Linkin Park',
		'New Metal',
		'1996',
		NULL,
		435261
	);

	INSERT INTO musico VALUES
	(
		'Ella Marija Lani Yelich-O''Connor',
		'Indie Pop',
		'19968-11-07',
		565758,
		NULL
	);

	INSERT INTO musico VALUES
	(
		'Michael Joseph Jackson',
		'Pop',
		'1958-08-29',
		789653,
		NULL
	);

	INSERT INTO musico VALUES
	(
		'Rammstein',
		'Industrial Metal',
		'1994',
		NULL,
		123543
	);

	INSERT INTO musico VALUES
	(
		'Queen',
		'Rock',
		'1970',
		NULL,
		4019283
	);