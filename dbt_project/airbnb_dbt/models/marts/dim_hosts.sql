{{ config(materialized='table') }}

SELECT DISTINCT
    host_id,
    host_name,
    is_superhost,
    response_rate
FROM {{ ref('stg_hosts') }}


-- {{ config(materialized='table') }}

-- SELECT *
-- FROM {{ ref('hosts_snapshot') }}
-- WHERE dbt_valid_to IS NULL