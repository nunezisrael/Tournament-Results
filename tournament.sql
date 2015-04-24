-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;

\c tournament;
	
<<<<<<< HEAD
drop table if exists players cascade;
	
=======
>>>>>>> origin/master
create table if not exists players (
id serial primary key unique not null, 
fullname text not null);

<<<<<<< HEAD
drop table if exists matches cascade;

=======
>>>>>>> origin/master
create table if not exists matches(
matchid serial primary key unique, 
matchNumber serial,
firstplayerid integer references players (id) ON DELETE CASCADE, 
secondplayerid integer references players (id) ON DELETE CASCADE);

<<<<<<< HEAD
drop table if exists playerstandings cascade;

create table if not exists playerstandings(
=======
create table if not exists playerStandings (
>>>>>>> origin/master
playerid integer REFERENCES players(id) ON DELETE CASCADE, 
wins integer DEFAULT 0, 
matches integer DEFAULT 0);

<<<<<<< HEAD
drop table if exists byestatus cascade;

create table if not exists byestatus (
playerid integer references players (id) ON DELETE CASCADE,
bye integer DEFAULT 0 CONSTRAINT single_bye CHECK (bye < 2));

create view pairs as
    select p.id,p.fullname,s.wins, s.matches
    from players as p join playerstandings as s
    on p.id = s.playerid
    order by s.wins desc,s.matches;
	
create view byeplayer as
	select p.playerid, pl.fullname, p.wins, p.matches
    from byestatus as b join playerstandings as p
    on b.playerid = p.playerid join players as pl
    on pl.id = p.playerid
    where b.bye = 0
    order by p.wins, b.bye desc;


=======
create table if not exists byestatus (
playerid integer references players (id) ON DELETE CASCADE,
bye integer DEFAULT 0 CONSTRAINT single_bye CHECK (bye < 2));
>>>>>>> origin/master
