import geopandas as gpd
from shapely import wkt


def shapeConverter(path_to_shape):
    gpdShape = gpd.read_file(path_to_shape)

    gpd_properties = gpdShape.columns.tolist()

    for i, prop in enumerate(gpd_properties, 1):
        print (f"{i} - {prop}")



    numeric_project_id_column = int(input("Favor inserir o número equivalente ao Nome do Talhão no Shapefile:"))
    project_id_column= gpd_properties[numeric_project_id_column-1]

    if gpdShape.crs != 'EPSG:3857':
        gpdShape = gpdShape.to_crs('EPSG:3857')

    wkt_conversions = []

    for idx, row in gpdShape.iterrows():
        id_projeto = row[project_id_column]
        geometry_wkt = wkt.dumps(row['geometry'])
        wkt_conversions.append((id_projeto, geometry_wkt))
    return wkt_conversions
