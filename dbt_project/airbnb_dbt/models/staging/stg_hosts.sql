{{ config(materialized='view') }}

SELECT
    "host_id"          AS host_id,
    TRIM("host_name")  AS host_name,
    "host_since"       AS host_since,
    "is_superhost"     AS is_superhost,
    "response_rate"    AS response_rate,
    "created_at"       AS created_at
FROM {{ source('raw', 'hosts_raw') }}
WHERE "host_id" IS NOT NULL