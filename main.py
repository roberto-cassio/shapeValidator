import shape_conversion
import intersection
import math
import credentials

import tkinter as tk
from tkinter import filedialog


#import GUI
#Volta Somente os Talhões que já Existem no Sistema
#Todos eles são pontos de atenção
#Se o id_projeto for diferente do recset[3] então adicionar um Atenção na última coluna, caso contrário deixar um OK
# Problema em encontrar alguns shapes com a query, verificar

def select_path():
    # Cria a janela oculta
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Abre o diálogo para seleção de arquivo
    file_path = filedialog.askopenfilename(title="Favor selecionar o local do Shapefile")

    return file_path

def show_menu():
    print("\nMenu de Opções")
    print("1. Verificar Talhões")
    print("2. Sair")

def verify_shapes():
    count = 1
    print(wkt_conversions[0])
    for item in intersection:
        rec_list = list(item)
        rec_list[-3] = f"{math.trunc(rec_list[-3] * 100)}%"
        rec_list[-2] = f"{math.trunc(rec_list[-2] * 100)}%"

        if not rec_list[1] and not rec_list[2]:
            rec_list.append("New")
            print(rec_list[5:])
            print(f'{count}/{len(intersection)}')
        elif rec_list[-1] != rec_list[2]:
            rec_list.append("Attention")
            print(rec_list[1:])
            print(f'{count}/{len(intersection)}')
        else:
            rec_list.append("OK")
            print(rec_list[1:])
            print(f'{count}/{len(intersection)}')

        count += 1
while True:
    show_menu()
    option = input("Escolha uma opção: ")

    if option == '1':
        client = input('Favor inserir a sigla do Cliente:')
        database = credentials.set_client(client)
        path = select_path()
        project_id_column = input('Nome do Talhão no Shapefile:')
        wkt_conversions = shape_conversion.shapeConverter(project_id_column, path)
        intersection = intersection.Intersection(wkt_conversions, database)

        id_projeto = [wkt[0] for wkt in wkt_conversions]
        verify_shapes()
    elif option == '2':
        print("Saindo...")
        break
    else:

        print("Opção inválida! Tente novamente.")



