{{ config(
    materialized = 'view',
    schema = 'staging'
) }}

with src as (
    select * from {{ source('landbay_raw', 'cases') }}
),

cleaned as (
    select
        cast (case_number as int64) as case_number,
        cast(lower(trim(broker_id)) as string) as broker_id,
        cast(lower(trim(broker_firm_id)) as string) as broker_firm_id,
        upper(trim(property_category)) as property_category,
        upper(trim(status)) as status,
        cast(loan_amount as float64) as loan_amount,
        --- Accepts second fractions of a second, and trims whitespace
        SAFE_CAST(PARSE_TIMESTAMP('%F %H:%M:%E*S', TRIM(application_submitted_date)) AS DATE) AS submitted_date,
        SAFE_CAST(PARSE_TIMESTAMP('%F %H:%M:%E*S', TRIM(completed_date)) AS DATE) AS completed_date,
        SAFE_CAST(PARSE_TIMESTAMP('%F %H:%M:%E*S', TRIM(cancellation_date)) AS DATE) AS cancellation_date
    
    from src

)

select *
from cleaned