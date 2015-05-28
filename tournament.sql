-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--terminating any active connections to the DB

SELECT
    pg_terminate_backend (pg_stat_activity.pid)
FROM
    pg_stat_activity
WHERE
    pg_stat_activity.datname = 'tournament';

drop database if exists tournament;
create database tournament;

\c tournament;

drop table if exists players cascade;

create table if not exists players(
player_id serial primary key unique,
fullname text not null);

drop table if exists matches cascade;

create table if not exists matches(
match_id serial primary key	unique,
p1 integer references players (player_id) ON DELETE CASCADE,
p2 integer references players (player_id) ON DELETE CASCADE);

create view total_matches as
	SELECT p.player_id, count(m.match_id) as total_matches
	FROM matches as m join players as p
	ON p.player_id = m.p1 or p.player_id = m.p2
	GROUP BY p.player_id;

create view wins as 
	SELECT p.player_id, count(m.match_id) as wins 
	FROM players as p join matches as m
	ON p.player_id = m.p1
	GROUP BY p.player_id;

create view standings as
	SELECT p.player_id, p.fullname, coalesce(w.wins,'0') as wins, coalesce(tm.total_matches,'0') as matches
	FROM total_matches as tm full outer join wins as w 
	ON tm.player_id = w.player_id full outer join players as p  
	ON p.player_id = tm.player_id 
	ORDER BY w.wins desc;
