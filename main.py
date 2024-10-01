import shape_conversion
import intersection
import math
#import GUI
#Volta Somente os Talhões que já Existem no Sistema
#Todos eles são pontos de atenção
#Se o id_projeto for diferente do recset[3] então adicionar um Atenção na última coluna, caso contrário deixar um OK
# Problema em encontrar alguns shapes com a query, verificar
project_id_column = input('Nome do Talhão no Shapefile:')
wkt_conversions = shape_conversion.shapeConverter(project_id_column)
intersection = intersection.Intersection(wkt_conversions)

id_projeto = [wkt[0] for wkt in wkt_conversions]

#GUI.MainScreen()

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





