-- Table definitions for the tournament project.

-- 0. Drop database "tournament if it exists"
DROP DATABASE IF EXISTS tournament;

-- 1. Create database "tournament" and connect to it
CREATE DATABASE tournament;
\c tournament

-- 2. Create table "players"
CREATE TABLE player_names (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  wins INT DEFAULT 0 CONSTRAINT non_negative_wins CHECK (wins >= 0),
  loses INT DEFAULT 0 CONSTRAINT non_negative_loses CHECK (loses >= 0)
);

CREATE TABLE stats ()

-- 3. Create table "matches"
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  -- reference to a SERIAL datatype must be an int
  winner INT REFERENCES players (id),
  loser INT REFERENCES players (id)
);

-- 4. Create a trigger to update players wins and loses
-- whenever "matches" is modified

-- The behavior being triggered
-- Case 1: INSERT
--         1. get new row winner and loser
--         2. update players with winner and loser id match
-- Case 2: DELETE
--         1. get old row winner and loser
--         2. update players with winner and loser id match
CREATE OR REPLACE FUNCTION update_scores_func() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN

        UPDATE players SET
            wins = (SELECT count(*) FROM matches WHERE matches.winner = players.id LIMIT 1)
        WHERE players.id = NEW.winner;

        UPDATE players SET
            loses = (SELECT count(*) FROM matches WHERE matches.loser = players.id LIMIT 1)
        WHERE players.id = NEW.loser;

        RETURN NEW;

    ELSIF (TG_OP = 'DELETE') THEN

        UPDATE players SET
            wins = (SELECT count(*) FROM matches WHERE matches.winner = players.id LIMIT 1)
        WHERE players.id = OLD.winner;

        UPDATE players SET
            loses = (SELECT count(*) FROM matches WHERE matches.loser = players.id LIMIT 1)
        WHERE players.id = OLD.loser;

        RETURN OLD;

    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_scores AFTER INSERT OR DELETE
  ON matches
  FOR EACH ROW
  EXECUTE PROCEDURE update_scores_func();
