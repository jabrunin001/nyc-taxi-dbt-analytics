-- 1. Which pickup boroughs generate the most daily revenue?
select *
from {{ ref('mart_daily_taxi_metrics') }}
order by gross_revenue desc;

-- 2. Which borough-to-borough routes have the highest average trip value?
select *
from {{ ref('mart_route_revenue') }}
order by avg_total_amount desc;

-- 3. How do tip rates vary by distance band?
select
    distance_band,
    round(avg(tip_share), 4) as avg_tip_share
from {{ ref('fct_taxi_trips') }}
group by 1
order by 1;
