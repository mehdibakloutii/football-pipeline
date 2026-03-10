with source as (
    select * from {{ source('public', 'matches') }}
),

renamed as (
    select
        id                  as match_id,
        competition_code,
        home_team,
        away_team,
        match_date,
        home_score,
        away_score,
        status,
        case
            when home_score > away_score then home_team
            when away_score > home_score then away_team
            else 'Draw'
        end as winner
    from source
    where status = 'FINISHED'
)

select * from renamed