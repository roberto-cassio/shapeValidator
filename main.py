from pandas.io.formats.format import return_docstring

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
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Favor selecionar o local do Shapefile (.zip)")

    return file_path

def select_output_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory(title="Favor selecionar o local onde o Shapefile será armazenado",
                                           filetypes=[("Arquivos ZIP", "*.zip")])

    return file_path
def show_menu():
    print("\nMenu de Opções")
    print("1. Verificar Talhões")
    print("2. Sair")


def verify_shapes():
    ok_shapes = []
    attention_shapes = []
    new_shapes = []

    count = 1
    for item in intersection:
        rec_list = list(item)
        rec_list[-3] = f"{math.trunc(rec_list[-3] * 100)}%"
        rec_list[-2] = f"{math.trunc(rec_list[-2] * 100)}%"

        if not rec_list[1] and not rec_list[2]:
            new_shapes.append(rec_list[5:])  # Armazena na lista de 'New'
        elif rec_list[-1] != rec_list[2]:
            attention_shapes.append(rec_list[1:])  # Armazena na lista de 'Attention'
        else:
            ok_shapes.append(rec_list[1:])  # Armazena na lista de 'OK'

        count += 1

    # Exibe as listas de forma separada
    print("\nShapes que existem mas estão OK para Subir:")
    for idx, shape in enumerate(ok_shapes, 1):
        print(f"{idx}: {shape}")

    print("\nShapes para se Atentar:")
    for idx, shape in enumerate(attention_shapes, 1):
        print(f"{idx}: {shape}")

    print("\nShapes Novos:")
    for idx, shape in enumerate(new_shapes, 1):
        print(f"{idx}: {shape}")

    return ok_shapes, new_shapes, attention_shapes


while True:
    show_menu()
    option = input("Escolha uma opção: ")

    if option == '1':
        client = input('Favor inserir a sigla do Cliente:')
        database = credentials.set_client(client)
        path = select_path()
        project_id,wkt_conversions = shape_conversion.shapeConverter(path)
        intersection = intersection.Intersection(wkt_conversions, database)

        id_projeto = [wkt[0] for wkt in wkt_conversions]
        ok_shapes, new_shapes, attention_shapes = verify_shapes()

        if len(attention_shapes) != 0:
            option2 = input("Deseja que o ShapeFiles dentro do padrão sejam removidos do ShapeFile? \n 1-Sim 2-Não")
            if option2 == '1':
                print ("Favor inserir o local de saída do novo Shapefile")
                output_path = select_output_path()
                shape_conversion.generate_new_shapefile(new_shapes, ok_shapes, path, project_id, output_path)
            else:
                show_menu()
    elif option == '2':
        print("Saindo...")
        break
    else:

        print("Opção inválida! Tente novamente.")



