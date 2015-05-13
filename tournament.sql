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

drop table if exists standings cascade;

create table if not exists standings(
player_id serial primary key unique,
fullname text not null,
wins integer DEFAULT 0,
matches integer DEFAULT 0);
