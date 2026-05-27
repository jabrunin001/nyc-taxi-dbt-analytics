select
    trip_id,
    pickup_at,
    dropoff_at,
    cast(pickup_at as date) as service_date,
    pickup_borough,
    dropoff_borough,
    passenger_count,
    trip_distance_miles,
    trip_duration_minutes,
    distance_band,
    payment_type,
    rate_code,
    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount,
    tip_share
from {{ ref('int_taxi_trip_metrics') }}
