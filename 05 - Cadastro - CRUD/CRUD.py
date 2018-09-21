#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2;
import psycopg2.extras;
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
#Métodos e Funções.


# Funcao de update de pessoas
# Permite editar nome, data de nascimento e cidade natal informando o login da pessoa
def update():
	# define o comando padrao em SQL para editar uma PESSOA
	update_pessoa = "UPDATE PESSOA SET update_name,update_date,update_home WHERE login = 'id'"
	update_name = ""
	update_date = ""
	update_home = ""

	# pede o login da pessoa ter seus dados modificados
	id = raw_input("Digite o login da pessoa que deseja modificar: ")
	stay = 1 # variavel de saida do loop

	while(stay):
		opcao = raw_input("O que deseja editar agora? \n 1 = Nome \n 2 = Data de nascimento \n 3 = Cidade natal \n 4 = Finalizar edição \n 5 = Cancelar \n")
		if(opcao == "1"):
			new_name = raw_input("Digite o novo nome: ") # pede o novo nome a ser inserido
			update_name = "nome_completo = 'new_name'"	# define a string de alteracao de nome
			update_name = update_name.replace("new_name", new_name)	# substitui o nome fornecido na string de alteracao de nome
		elif(opcao == "2"):
			new_date = raw_input("Digite a nova data de nascimento no formato dia/mes/ano: ") # pede a nova data de nascimento nome a ser inserido
			update_date = "data_nascimento = 'new_date'" # define a string de alteracao de data
			update_date = update_date.replace("new_date", new_date) # substitui a data fornecida na string de alteracao de data
		elif(opcao == "3"):
			new_home = raw_input("Digite a nova cidade natal: ") # pede a nova cidade natal a ser inserido
			update_home = "cidade_natal = 'new_home'" # define a string de alteracao de cidade
			update_home = update_home.replace("new_home", new_home) # substitui a cidade fornecida na string de alteracao de cidade
		elif(opcao == "4"):
			update_pessoa = update_pessoa.replace("id", id) # substitui o login na string de update
			update_pessoa = update_pessoa.replace("update_name", update_name) # substitui o novo nome na string de update
			update_pessoa = update_pessoa.replace("update_date", update_date) # substitui a nova data na string de update
			update_pessoa = update_pessoa.replace("update_home", update_home) # substitui a nova cidade na string de update
			update_pessoa = update_pessoa.replace("SET ,,", "SET ") # exclui caso estejam sobrando virgulas
			update_pessoa = update_pessoa.replace("SET ,", "SET ") # exclui caso estejam sobrando virgulas
			update_pessoa = update_pessoa.replace(",, WHERE", " WHERE") # exclui caso estejam sobrando virgulas
			update_pessoa = update_pessoa.replace(", WHERE", " WHERE") # exclui caso estejam sobrando virgulas

			stay = 0 # para sair do loop
		elif(opcao == "5"):
			update_pessoa = "" # update cancelado, string de update apagada
			stay = 0 # para sair do loop
		else:
			print("Digite uma opcao valida.\n")

	return update_pessoa;

def delete():
	LoginPessoa = raw_input("Digite o login da pessoa que deseja apagar: ")
	delete_pessoa = "DELETE FROM Pessoa WHERE pessoa.login LIKE '" + LoginPessoa + "';"
	return delete_pessoa;

def listagem():
	listar_pessoas = "SELECT * FROM Pessoa;"
	return listar_pessoas;

def inserir():
	inserir_pessoas = "INSERT INTO Pessoa VALUES ('pessoa.id','pessoa.nome','pessoa.cidade_natal','pessoa.anonascimento'); "
	new_id = raw_input("Digite o login: ")
	new_name = raw_input("Digite o nome:  ")
	new_city = raw_input("Digite a cidade natal: ")
	new_nasc = raw_input("Digite o ano de nascimento no padrão dia/mês/ano: ")
	inserir_pessoas = inserir_pessoas.replace("pessoa.id",new_id)
	inserir_pessoas = inserir_pessoas.replace("pessoa.nome",new_name)
	inserir_pessoas = inserir_pessoas.replace("pessoa.cidade_natal",new_city)
	inserir_pessoas = inserir_pessoas.replace("pessoa.anonascimento",new_nasc)

	return inserir_pessoas;


#Flags para o chaveamento dos menus. Acredito que talvez com um break; continue; daria certo também.
menu1_on = True;
menu2_on = True;
end = False;

#Teste de conexão
try:
	conn = psycopg2.connect("dbname='1802BandoDeDados' user='1802BandoDeDados' host='200.134.10.32' password='803322'")
except:
	print "Falha ao se conectar ao banco de dados. Terminando o programa..."
	end = True;

while menu1_on and not end:
	option = raw_input("O que deseja fazer? \n 1 - Listar todas as pessoas \n 2 - Cadastrar uma nova pessoa \n 3 - Sair do programa.  \n Digite o valor da opção que deseja. \n")
	if option=="1":
		print(" \n Listando...  \n")
		conn.set_client_encoding('LATIN9')
		cur = conn.cursor()
		try:
			cur.execute(listagem())
			for pessoas in cur:
				print(unicode(unicode(pessoas[0]) + ", " + unicode(pessoas[1]) + ", " + unicode(pessoas[2]) + ", " + unicode(pessoas[3])))
		except:
			print("Falha ao Listar.")
		conn.commit()
		cur.close()
		while  menu2_on:
			option2 = raw_input("O que deseja fazer agora? \n 1 - Voltar \n 2 - Apagar uma pessoa \n 3 - Editar uma pessoa. \n")
			if option2=="1":
				print("\n Voltando... \n")
				menu2_on = False; #Sai do menu 2.
			elif option2=="2":
				print("\n Carregando... \n")
				cur = conn.cursor()
				cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
				try:
					cur.execute(delete())
				except:
					print("Falha ao deletar")
				conn.commit()
 				cur.close()
			elif option2=="3": #Opção de Editar (Update)
				print("\n Carregando... \n")
				cur = conn.cursor()
				cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
				try:
					cur.execute(update())
				except:
					print("Falha ao dar update.")
				conn.commit()
				cur.close()
			else:
				print("\n Digite uma opção válida! \n")
		menu2_on = True; #Reconfigura menu 2.
	elif option =="2":
		print("\n Carregando... \n")
		cur = conn.cursor()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		try:
			cur.execute(inserir())
		except:
			print("Falha ao  inserir.")
		conn.commit()
		cur.close()
	elif option=="3":
		print(" \n Saindo... \n")
		menu1_on = False
	else:
		print("Digite uma opção válida!")

#Ao encerrar o programa, fecha a conexão com o banco.
conn.close()