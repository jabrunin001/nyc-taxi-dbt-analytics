select
    pickup_borough,
    dropoff_borough,
    distance_band,
    count(*) as trip_count,
    round(sum(total_amount), 2) as gross_revenue,
    round(avg(total_amount), 2) as avg_total_amount,
    round(avg(tip_share), 4) as avg_tip_share
from {{ ref('fct_taxi_trips') }}
group by 1, 2, 3
