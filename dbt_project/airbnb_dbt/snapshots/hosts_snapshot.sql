{% snapshot hosts_snapshot %}

{{
    config(
        target_schema='SNAPSHOTS',
        unique_key='host_id',
        strategy='check',
        check_cols=['host_name', 'is_superhost', 'response_rate']
    )
}}

SELECT
    host_id,
    host_name,
    is_superhost,
    response_rate,
    host_since,
    created_at
FROM {{ ref('stg_hosts') }}

{% endsnapshot %}