{{ config(materialized='table') }}

SELECT DISTINCT
    listing_id,
    host_id,
    property_type,
    room_type,
    city,
    country,
    price_per_night
FROM {{ ref('stg_listings') }}