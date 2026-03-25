{{ config(materialized='table') }}

SELECT
    b.booking_id,
    b.booking_date,
    b.nights_booked,
    b.booking_amount,
    b.cleaning_fee,
    b.service_fee,
    b.booking_status,
    b.created_at as booking_created_at,   -- ✅ ADD THIS

    l.listing_id,
    l.property_type,
    l.room_type,
    l.city,
    l.country,
    l.price_per_night,

    h.host_id,
    h.host_name,
    h.is_superhost,
    h.response_rate

FROM {{ ref('stg_bookings') }} b
LEFT JOIN {{ ref('stg_listings') }} l
    ON b.listing_id = l.listing_id
LEFT JOIN {{ ref('stg_hosts') }} h
    ON l.host_id = h.host_id