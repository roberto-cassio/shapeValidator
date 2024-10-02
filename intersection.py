import psycopg2 as psycopg
import credentials

rec_list_all = []
def Intersection(wkt_conversion, database):
    connection = psycopg.connect(host=credentials.host, database=database, user=credentials.user, password=credentials.password)
    cursor = connection.cursor()
    for index, (id_projeto, geometry_wkt) in enumerate(wkt_conversion):
        sql=f'''
        WITH area_temp AS (
            SELECT ST_GeomFromText('{geometry_wkt}', 3857) AS area
        ),
        intersection_area AS (
            SELECT
                a.area AS area,
                l1.id AS location1_id,
                l1.name AS location1_name,
                CASE
                    WHEN ST_Area(ST_Intersection(l1.area, a.area)) = 0 THEN 0
                    ELSE ST_Area(ST_Intersection(l1.area, a.area)) / ST_Area(l1.area)
                END AS intersection_area_location_1,
                CASE
                    WHEN ST_Area(ST_Intersection(l1.area, a.area)) = 0 THEN 0
                    ELSE ST_Area(ST_Intersection(l1.area, a.area)) / ST_Area(a.area)
                END AS intersection_area_location_2
            FROM
                operation."location" l1
                CROSS JOIN area_temp a
            WHERE
                ST_IsValid(l1.area)
                AND l1.deleted_at IS NULL
                AND ST_SRID(l1.area) = 3857
        )
        SELECT *
        FROM intersection_area
        WHERE
            intersection_area_location_1 > 0.6
            AND intersection_area_location_2 > 0.6;'''

        cursor.execute(sql)
        rec_list = cursor.fetchall()

        print(f"Progresso: {100 * (index + 1) / len(wkt_conversion):.2f}%")
        if rec_list:
            for rec in rec_list:
                rec_with_id = list(rec) + [id_projeto]
                rec_list_all.append(rec_with_id)
        else:
            rec_list_all.append([None, None, None, 0, 0, id_projeto])
    connection.close()
    return rec_list_all

