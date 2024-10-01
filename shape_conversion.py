import geopandas as gpd
from shapely import wkt

def shapeConverter(project_id_column):
    gpdShape = gpd.read_file('SHP/GEO_AMBIO_AREA_PRODUTIVA.zip')



    if gpdShape.crs != 'EPSG:3857':
        gpdShape = gpdShape.to_crs('EPSG:3857')

    wkt_conversions = []

    for idx, row in gpdShape.iterrows():
        id_projeto = row[project_id_column]
        geometry_wkt = wkt.dumps(row['geometry'])
        wkt_conversions.append((id_projeto, geometry_wkt))
    return wkt_conversions
