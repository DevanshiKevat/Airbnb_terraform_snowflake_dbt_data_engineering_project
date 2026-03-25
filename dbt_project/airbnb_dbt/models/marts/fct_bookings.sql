{{ config(
    materialized='incremental',
    unique_key='booking_id',
    incremental_strategy='merge'
) }}

SELECT
    booking_id,
    booking_date,
    listing_id,
    host_id,
    nights_booked,
    booking_amount,
    cleaning_fee,
    service_fee,
    booking_status,

    booking_amount + cleaning_fee + service_fee AS total_revenue,
    nights_booked * price_per_night AS expected_revenue, 
    booking_created_at

FROM {{ ref('int_booking_enriched') }}

{% if is_incremental() %}

WHERE booking_created_at > (
    SELECT MAX(booking_created_at)
    FROM {{ this }}
)

{% endif %}