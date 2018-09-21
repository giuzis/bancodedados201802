#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2;

#Flags para o chaveamento dos menus. Acredito que talvez com um break; continue; daria certo também.
menu1_on = True;
menu2_on = True;

while menu1_on:
	option = raw_input("O que deseja fazer? \n 1 - Listar todas as pessoas \n 2 - Cadastrar uma nova pessoa \n 3 - Sair do programa.  \n Digite o valor da opção que deseja. \n")
	if option=="1":
		print(" \n Listando...  \n")
		while  menu2_on:
			option2 = raw_input("O que deseja fazer agora? \n 1 - Voltar \n 2 - Apagar uma pessoa \n 3 - Editar uma pessoa. \n")
			if option2=="1":
				print("\n Voltando... \n")
				menu2_on = False; #Sai do menu 2.
			elif option2=="2":
				print("\n Carregando... \n")
			elif option2=="3":
				print("\n Carregando... \n")
			else:
				print("\n Digite uma opção válida! \n")
		menu2_on = True; #Reconfigura menu 2.
	elif option =="2":
		print("\n Carregando... \n")
	elif option=="3":
		print(" \n Saindo... \n")
		menu1_on = False
	else:
		print("Digite uma opção válida!")
