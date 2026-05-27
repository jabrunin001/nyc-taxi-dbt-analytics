select
    service_date,
    pickup_borough,
    count(*) as trip_count,
    sum(passenger_count) as passenger_count,
    round(sum(total_amount), 2) as gross_revenue,
    round(avg(total_amount), 2) as avg_total_amount,
    round(avg(trip_distance_miles), 2) as avg_trip_distance_miles,
    round(avg(trip_duration_minutes), 2) as avg_trip_duration_minutes,
    round(avg(tip_share), 4) as avg_tip_share
from {{ ref('fct_taxi_trips') }}
group by 1, 2
