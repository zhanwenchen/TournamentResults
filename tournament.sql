-- Table definitions for the tournament project.

-- 0. Drop database "tournament if it exists"
DROP DATABASE IF EXISTS tournament;

-- 1. Create database "tournament" and connect to it
CREATE DATABASE tournament;
\c tournament

-- 2. Create table "players"
CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT,
  wins INT DEFAULT 0 CONSTRAINT non_negative_wins CHECK (wins >= 0),
  loses INT DEFAULT 0 CONSTRAINT non_negative_loses CHECK (loses >= 0)
);

-- 3. Create table "matches"
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  -- reference to a SERIAL datatype must be an int
  win INT REFERENCES players (id),
  lose INT REFERENCES players (id)
);

-- 4. Create a view using "CREATE VIEW"
