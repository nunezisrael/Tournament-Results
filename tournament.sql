-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;

\c tournament;
	
create table if not exists players (
id serial primary key unique not null, 
fullname text not null);

create table if not exists matches(
matchid serial primary key unique, 
matchNumber serial,
firstplayerid integer references players (id) ON DELETE CASCADE, 
secondplayerid integer references players (id) ON DELETE CASCADE);

create table if not exists playerStandings (
playerid integer REFERENCES players(id) ON DELETE CASCADE, 
wins integer DEFAULT 0, 
matches integer DEFAULT 0);

create table if not exists byestatus (
playerid integer references players (id) ON DELETE CASCADE,
bye integer DEFAULT 0 CONSTRAINT single_bye CHECK (bye < 2));
