{{ config(materialized='view') }}

SELECT
    "listing_id"        AS listing_id,
    "host_id"           AS host_id,
    "property_type"     AS property_type,
    "room_type"         AS room_type,
    "city"              AS city,
    "country"           AS country,
    "accommodates"      AS accommodates,
    "bedrooms"          AS bedrooms,
    "bathrooms"         AS bathrooms,
    "price_per_night"   AS price_per_night,
    "created_at"        AS created_at
FROM {{ source('raw', 'listings_raw') }}