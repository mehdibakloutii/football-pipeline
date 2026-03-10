with matches as (
    select * from {{ ref('stg_matches') }}
),

home_stats as (
    select
        home_team as team,
        count(*) as games_played,
        sum(case when winner = home_team then 1 else 0 end) as wins,
        sum(case when winner = 'Draw' then 1 else 0 end) as draws,
        sum(case when winner = away_team then 1 else 0 end) as losses,
        sum(home_score) as goals_scored,
        sum(away_score) as goals_conceded
    from matches
    group by home_team
),

away_stats as (
    select
        away_team as team,
        count(*) as games_played,
        sum(case when winner = away_team then 1 else 0 end) as wins,
        sum(case when winner = 'Draw' then 1 else 0 end) as draws,
        sum(case when winner = home_team then 1 else 0 end) as losses,
        sum(away_score) as goals_scored,
        sum(home_score) as goals_conceded
    from matches
    group by away_team
),

combined as (
    select * from home_stats
    union all
    select * from away_stats
),

final as (
    select
        team,
        sum(games_played)   as games_played,
        sum(wins)           as wins,
        sum(draws)          as draws,
        sum(losses)         as losses,
        sum(goals_scored)   as goals_scored,
        sum(goals_conceded) as goals_conceded,
        sum(wins) * 3 + sum(draws) as points
    from combined
    group by team
    order by points desc
)

select * from final