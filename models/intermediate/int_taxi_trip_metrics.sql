with trips as (
    select *
    from {{ ref('stg_taxi_trips') }}
),

metrics as (
    select
        trip_id,
        pickup_at,
        dropoff_at,
        pickup_borough,
        dropoff_borough,
        passenger_count,
        trip_distance_miles,
        fare_amount,
        tip_amount,
        tolls_amount,
        total_amount,
        payment_type,
        rate_code,
        date_diff('minute', pickup_at, dropoff_at) as trip_duration_minutes,
        case
            when trip_distance_miles < 2 then 'short'
            when trip_distance_miles < 6 then 'medium'
            else 'long'
        end as distance_band,
        case
            when total_amount = 0 then 0
            else round(tip_amount / total_amount, 4)
        end as tip_share
    from trips
)

select *
from metrics
