import requests
import psycopg2
from psycopg2.extras import execute_values

POSTGRES_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "temp_db",
    "user": "admin",
    "password": "admin",
}

RESOURCE_ID = "0e3b6840-7dff-4731-a556-44fac28a7873"
API_URL = f"https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search"
LIMIT = 1000  # número máximo de filas por llamada (CKAN soporta hasta 1000)

# Tabla destino
TABLE_NAME = "barcelona_monthly_temp"


def create_table(conn):
    sql = f"""
    CREATE TABLE IF NOT EXISTS public.{TABLE_NAME} (
        any_year INTEGER PRIMARY KEY,
        temp_gener FLOAT,
        temp_febrer FLOAT,
        temp_marc FLOAT,
        temp_abril FLOAT,
        temp_maig FLOAT,
        temp_juny FLOAT,
        temp_juliol FLOAT,
        temp_agost FLOAT,
        temp_setembre FLOAT,
        temp_octubre FLOAT,
        temp_novembre FLOAT,
        temp_desembre FLOAT
    );
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def fetch_all_records():
    """Obtiene todos los registros de la API CKAN paginando por 'offset'"""
    all_records = []
    offset = 0
    while True:
        params = {
            "resource_id": RESOURCE_ID,
            "limit": LIMIT,
            "offset": offset
        }
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data["result"]["records"]
        if not records:
            break
        all_records.extend(records)
        offset += LIMIT
    return all_records


def insert_records(conn, records):
    sql = f"""
        INSERT INTO public.{TABLE_NAME} (
            any_year, temp_gener, temp_febrer, temp_marc, temp_abril, temp_maig,
            temp_juny, temp_juliol, temp_agost, temp_setembre, temp_octubre,
            temp_novembre, temp_desembre
        )
        VALUES %s
        ON CONFLICT (any_year) DO UPDATE SET
            temp_gener = EXCLUDED.temp_gener,
            temp_febrer = EXCLUDED.temp_febrer,
            temp_marc = EXCLUDED.temp_marc,
            temp_abril = EXCLUDED.temp_abril,
            temp_maig = EXCLUDED.temp_maig,
            temp_juny = EXCLUDED.temp_juny,
            temp_juliol = EXCLUDED.temp_juliol,
            temp_agost = EXCLUDED.temp_agost,
            temp_setembre = EXCLUDED.temp_setembre,
            temp_octubre = EXCLUDED.temp_octubre,
            temp_novembre = EXCLUDED.temp_novembre,
            temp_desembre = EXCLUDED.temp_desembre;
    """
    values = [
        (
            r["Any"],
            float(r["Temp_Mitjana_Gener"]) if r["Temp_Mitjana_Gener"] else None,
            float(r["Temp_Mitjana_Febrer"]) if r["Temp_Mitjana_Febrer"] else None,
            float(r["Temp_Mitjana_Marc"]) if r["Temp_Mitjana_Marc"] else None,
            float(r["Temp_Mitjana_Abril"]) if r["Temp_Mitjana_Abril"] else None,
            float(r["Temp_Mitjana_Maig"]) if r["Temp_Mitjana_Maig"] else None,
            float(r["Temp_Mitjana_Juny"]) if r["Temp_Mitjana_Juny"] else None,
            float(r["Temp_Mitjana_Juliol"]) if r["Temp_Mitjana_Juliol"] else None,
            float(r["Temp_Mitjana_Agost"]) if r["Temp_Mitjana_Agost"] else None,
            float(r["Temp_Mitjana_Setembre"]) if r["Temp_Mitjana_Setembre"] else None,
            float(r["Temp_Mitjana_Octubre"]) if r["Temp_Mitjana_Octubre"] else None,
            float(r["Temp_Mitjana_Novembre"]) if r["Temp_Mitjana_Novembre"] else None,
            float(r["Temp_Mitjana_Desembre"]) if r["Temp_Mitjana_Desembre"] else None,
        )
        for r in records
    ]
    with conn.cursor() as cur:
        execute_values(cur, sql, values)
    conn.commit()


def main():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    print("Conectado a PostgreSQL")

    create_table(conn)
    print("Tabla creada / verificada")

    records = fetch_all_records()
    print(f"Registros obtenidos: {len(records)}")

    insert_records(conn, records)
    print("Registros insertados/actualizados en la base de datos")

    conn.close()


if __name__ == "__main__":
    main()
