# Elementary Data Project

## Introducción

Elementary es una herramienta de *data observability* que permite monitorear, detectar y diagnosticar problemas en los datos antes de que impacten en los usuarios finales. Se integra directamente con **dbt**, aprovechando sus modelos, tests y metadatos para generar métricas de observabilidad de forma automática.

Con esta integración, Elementary puede identificar anomalías como cambios inesperados en el volumen de datos, valores nulos, inconsistencias, problemas de frescura o fallos en los tests de dbt. La herramienta está diseñada para trabajar sobre **data warehouses** modernos como Postgres, BigQuery, Snowflake o Databricks, sin necesidad de mover los datos fuera del entorno del cliente.

Elementary también ofrece monitoreo histórico, alertas y análisis de causa raíz, facilitando el mantenimiento y la confiabilidad de los pipelines de datos en producción.

<p align="center"> 
  <img src="./imagenes/Captura_3.png"/> 
</p>

## Configuración del entorno

Para comenzar, creamos un entorno virtual de Python y lo activamos:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Actualizamos pip y luego instalamos dbt y Elementary:

```bash
pip install --upgrade pip
pip install dbt-postgres elementary-data
```

### Estructura del proyecto dbt

El proyecto contiene:

* **models/sources.yml**: definición de la fuente `barcelona_temp_source` apuntando a `temp_db.public.barcelona_monthly_temp`.
* **models/staging/stg_barcelona_temp.sql**: modelo de staging que limpia y selecciona las columnas necesarias.
* **models/staging/stg_barcelona_temp.yml**: esquema de staging con tests de integridad.
* **models/marts/agg_barcelona_temp.sql**: modelo que genera métricas agregadas.
* **models/marts/agg_barcelona_temp.yml**: esquema del modelo de métricas agregadas con tests de integridad.

## Integración de Elementary con dbt

Para integrar Elementary:

1. Añadir a **packages.yml**:

```yaml
packages:
  - package: elementary-data/elementary
    version: 0.15.2
```

2. Instalar dependencias:

```bash
dbt deps
```

3. Configurar el esquema donde Elementary almacenará sus métricas en **dbt_project.yml** y activar flags necesarios.

```yaml
  elementary:
    +schema: "elementary"
```

4. Conectar Elementary al warehouse configurando **profiles.yml**. Esto permite que Elementary lea los artifacts de dbt (`manifest.json`, `run_results.json`) y genere métricas de observabilidad sin mover los datos.

5. Generar el perfil de Elementary:

```bash
dbt run-operation elementary.generate_elementary_cli_profile --profiles-dir C:\Users\{user}\.dbt
```

* Nota Instalar Elementary de forma específica si fuera necesario para otra plataforma (Postgres no requiere este paso):
  ```bash
  pip install 'elementary-data[bigquery]'
  ```

## Datos y dashboards sin errores

Después de ejecutar los modelos de dbt:

```bash
dbt run
dbt test
```

Vista de la tabla y dos views en Postgres:

<p align="center"> 
  <img src="./imagenes/Captura_1.png"/> 
</p>

Tabla `stg` en Postgres:

<p align="center"> 
  <img src="./imagenes/Captura_4.png"/> 
</p>

Tabla `agg` en Postgres:

<p align="center"> 
  <img src="./imagenes/Captura_5.png"/> 
</p>

Ejecutando `dbt run --select elementary`:

<p align="center"> 
  <img src="./imagenes/Captura_2.png"/> 
</p>

Ejecutando `edr report` Dashboard de Elementary con todos los tests pasados:

<p align="center"> 
  <img src="./imagenes/Captura_0.png"/> 
</p>

## Incorporación de errores

Se añaden valores erróneos para probar la detección de anomalías:

<p align="center"> 
  <img src="./imagenes/Captura_6.png"/> 
</p>

Datos de la tabla original con filas afectadas por valores nulos y atípicos:

<p align="center"> 
  <img src="./imagenes/Captura_7.png"/> 
</p>

## Visualización de errores en Elementary

Después de añadir los errores, se vuelve a ejecutar:

```bash
dbt run
dbt test
dbt run --select elementary
edr report
```

Dashboard de Elementary mostrando los tests en rojo:

<p align="center"> 
  <img src="./imagenes/Captura_8.png"/> 
</p>

Tests de la tabla source que no pasaron:

<p align="center"> 
  <img src="./imagenes/Captura_9.png"/> 
</p>

Tests de la vista `stg` que no pasaron:

<p align="center"> 
  <img src="./imagenes/Captura_10.png"/> 
</p>

Tests de la vista `agg` que no pasaron:

<p align="center"> 
  <img src="./imagenes/Captura_11.png"/> 
</p>

Este flujo muestra cómo Elementary puede integrarse con dbt para:

* Monitorear la calidad de los datos automáticamente.
* Detectar anomalías antes de impactar a usuarios.
* Visualizar el estado de los tests de manera centralizada.


