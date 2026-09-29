-- One row per census tract with a simple food access score.
-- Placeholder logic: swap in a real distance-to-nearest-grocery calc later.
select
    c.tract,
    c.tract_name,
    c.median_household_income,
    c.total_population,
    count(s.name) as nearby_grocery_count
from {{ ref('stg_census') }} c
left join {{ ref('stg_stores') }} s
    on s.category = 'grocery store'
group by 1, 2, 3, 4
