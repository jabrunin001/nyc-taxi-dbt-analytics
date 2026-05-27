with source as (
    select *
    from {{ ref('raw_taxi_trips') }}
),

typed as (
    select
        cast(trip_id as integer) as trip_id,
        cast(pickup_datetime as timestamp) as pickup_at,
        cast(dropoff_datetime as timestamp) as dropoff_at,
        trim(pickup_borough) as pickup_borough,
        trim(dropoff_borough) as dropoff_borough,
        cast(passenger_count as integer) as passenger_count,
        cast(trip_distance as decimal(10, 2)) as trip_distance_miles,
        cast(fare_amount as decimal(10, 2)) as fare_amount,
        cast(tip_amount as decimal(10, 2)) as tip_amount,
        cast(tolls_amount as decimal(10, 2)) as tolls_amount,
        cast(total_amount as decimal(10, 2)) as total_amount,
        lower(trim(payment_type)) as payment_type,
        lower(trim(rate_code)) as rate_code
    from source
)

select *
from typed
where pickup_at < dropoff_at
  and total_amount >= 0
  and trip_distance_miles >= 0
