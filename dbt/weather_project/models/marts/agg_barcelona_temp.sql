-- Métricas agregadas por año
select
    any_year,
    (temp_gener + temp_febrer + temp_marc + temp_abril + temp_maig + temp_juny + 
     temp_juliol + temp_agost + temp_setembre + temp_octubre + temp_novembre + temp_desembre) / 12 as temp_media_anual,
    temp_gener as temp_gener,
    temp_febrer as temp_febrer,
    temp_marc as temp_marc,
    temp_abril as temp_abril,
    temp_maig as temp_maig,
    temp_juny as temp_juny,
    temp_juliol as temp_juliol,
    temp_agost as temp_agost,
    temp_setembre as temp_setembre,
    temp_octubre as temp_octubre,
    temp_novembre as temp_novembre,
    temp_desembre as temp_desembre
from {{ ref('stg_barcelona_temp') }}
order by any_year
