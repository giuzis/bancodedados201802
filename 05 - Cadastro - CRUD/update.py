

# Funcao de update de pessoas
# Permite editar nome, data de nascimento e cidade natal informando o login da pessoa
def update():
	# define o comando padrao em SQL para editar uma PESSOA
	update_pessoa = "UPDATE PESSOA SET update_name,update_date,update_home WHERE login = 'id'"
	update_name = ""
	update_date = ""
	update_home = ""
	
	# pede o login da pessoa ter seus dados modificados
	id = raw_input("Digite a login da pessoa que deseja modificar: ")
	stay = 1 # variavel de saida do loop

	while(stay):
		opcao = raw_input("O que deseja editar agora? \n 1 = Nome \n 2 = Data de nascimento \n 3 = Cidade natal \n 4 = Finalizar edicao \n 5 = Cancelar \n")
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