{{ config(materialized='view') }}

SELECT
    "booking_id"        AS booking_id,
    "listing_id"        AS listing_id,
    "booking_date"      AS booking_date,
    "nights_booked"     AS nights_booked,
    "booking_amount"    AS booking_amount,
    "cleaning_fee"      AS cleaning_fee,
    "service_fee"       AS service_fee,
    "booking_status"    AS booking_status,
    "created_at"        AS created_at
FROM {{ source('raw', 'bookings_raw') }}
WHERE "booking_id" IS NOT NULL