-- Selección de los datos desde la fuente
select
    any_year,
    temp_gener,
    temp_febrer,
    temp_marc,
    temp_abril,
    temp_maig,
    temp_juny,
    temp_juliol,
    temp_agost,
    temp_setembre,
    temp_octubre,
    temp_novembre,
    temp_desembre
from {{ source('barcelona_temp_source', 'barcelona_monthly_temp') }}
