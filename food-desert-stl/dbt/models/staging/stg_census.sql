-- Cleans up raw census tract data
select
    name as tract_name,
    tract,
    cast(median_household_income as int64) as median_household_income,
    cast(total_population as int64) as total_population
from {{ source('raw', 'census') }}
