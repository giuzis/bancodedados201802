#!/usr/bin/env python
# -*- coding: utf-8 -*-
from imdb import IMDb
import psycopg2
#For Special Characters
import sys
reload(sys)
sys.setdefaultencoding('utf8')

filmes_imdb = IMDb()
filme = filmes_imdb.get_movie('0068646')
filmes_imdb.update(filme, info=['main', 'release dates'])
nome_s = filme.get('main')
data_s = filme.get('release dates')
#categoria_s =
print(nome_s , data_s)