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
	
create table if not exists players (
id serial primary key unique not null, 
fullname text not null,
wins integer DEFAULT 0,
matches integer DEFAULT 0);

drop table if exists matches cascade;

create table if not exists matches(
matchid serial primary key unique, 
firstplayerid integer references players (id) ON DELETE CASCADE, 
secondplayerid integer references players (id) ON DELETE CASCADE,
winner integer,
loser integer);

drop table if exists byestatus cascade;

create table if not exists byestatus (
playerid integer references players (id) ON DELETE CASCADE,
bye integer DEFAULT 0 CONSTRAINT single_bye CHECK (bye < 2));
	
create view byeplayer as
	select p.id, p.fullname, p.wins, p.matches
    from byestatus as b join players as p
    on b.playerid = p.id
    where b.bye = 0
    order by p.wins, b.bye desc;
