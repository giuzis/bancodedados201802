import psycopg2;

flag = 1;
flag2 = 1;
while(flag == 1):
	menu =  raw_input("O que quer fazer agora? \n 1 = Listar \n 2 = Cadastrar\n 3 = Sair \n")
	if(menu == "1"):
		print("Listando...! \n")
		menu2 = raw_input("O que quer fazer agora? \n 1 = Editar \n 2 = Apagar \n 3 = Sair \n"")
		while(flag2 == 1)
			if(menu2 == "1"):
				print("Editando...! \n")
			elif(menu2 == "2"):
				print("Apagando...! \n")
			elif(menu2 == "3"):
				print("Saindo...! \n")
				flag2 = 0
			else:
				print("Digite um numero valido!")
	elif(menu == "2"):
		print("Cadastrado! \n")
	elif(menu == "3"):
		print("Saindo...! \n")
		flag = 0
	else:
		print("Digite um numero valido!")
print("Ate logo...")
