-- Cleans up raw store locations loaded from GCS into BigQuery
select
    name,
    category,
    lat,
    lng,
    address
from {{ source('raw', 'places') }}
where lat is not null and lng is not null
