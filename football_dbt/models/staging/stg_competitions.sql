with source as (
    select * from {{ source('public', 'competitions') }}
),

renamed as (
    select
        id              as competition_id,
        name            as competition_name,
        code            as competition_code,
        country
    from source
)

select * from renamed