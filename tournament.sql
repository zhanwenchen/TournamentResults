-- Table definitions for the tournament project.

-- 0. Drop database "tournament if it exists"
DROP DATABASE IF EXISTS tournament;

-- 1. Create database "tournament" and connect to it
CREATE DATABASE tournament;
\c tournament

-- 2. Create table "player_names"
CREATE TABLE player_names (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

-- 3. Create table "player_scores"
CREATE TABLE player_scores (
  id INT REFERENCES player_names (id),
  wins INT DEFAULT 0 CONSTRAINT non_negative_wins CHECK (wins >= 0),
  loses INT DEFAULT 0 CONSTRAINT non_negative_loses CHECK (loses >= 0)
);

-- 4. Create table "matches"
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  -- reference to a SERIAL datatype must be an int
  winner INT REFERENCES player_names (id),
  loser INT REFERENCES player_names (id)
);

-- 5. Create a trigger to update players wins and loses
-- whenever "player_names" is modified

-- Behaviors triggered
-- Case 1: ON "INSERT"
--         1. Insert a new row with default values
-- Case 2: ON "DELETE"
--         1. Delete the row with the same id
CREATE OR REPLACE FUNCTION update_scores_wrt_registration_func() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN

        INSERT INTO player_scores
            (id)
        VALUES
            (NEW.id);

        RETURN NEW;

    ELSIF (TG_OP = 'DELETE') THEN

        DELETE FROM player_scores
        WHERE player_scores.id = OLD.id;

        RETURN OLD;

    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create separate triggers for BEFORE INSERT and AFTER DELETE in player_names
-- due to foreign key constraints in player_scores
CREATE TRIGGER update_scores_wrt_registration_insert AFTER INSERT
  ON player_names
  FOR EACH ROW
  EXECUTE PROCEDURE update_scores_wrt_registration_func();

CREATE TRIGGER update_scores_wrt_registration_delete BEFORE DELETE
  ON player_names
  FOR EACH ROW
  EXECUTE PROCEDURE update_scores_wrt_registration_func();

  -- 6. Create a trigger to update players wins and loses
  -- whenever "matches" is modified

  -- The behavior being triggered
  -- Case 1: INSERT
  --         1. get new row winner and loser
  --         2. update players with winner and loser id match
  -- Case 2: DELETE
  --         1. get old row winner and loser
  --         2. update players with winner and loser id match
  CREATE OR REPLACE FUNCTION update_scores_wrt_match_func() RETURNS TRIGGER AS $$
  BEGIN
      IF (TG_OP = 'INSERT') THEN

          UPDATE player_scores SET
              wins = (SELECT count(*) FROM matches WHERE matches.winner = player_scores.id LIMIT 1)
          WHERE player_scores.id = NEW.winner
          ;

          UPDATE player_scores SET
              loses = (SELECT count(*) FROM matches WHERE matches.loser = player_scores.id LIMIT 1)
          WHERE player_scores.id = NEW.loser
          ;

          RETURN NEW;

      ELSIF (TG_OP = 'DELETE') THEN

          UPDATE player_scores SET
              wins = (SELECT count(*) FROM matches WHERE matches.winner = player_scores.id LIMIT 1)
          WHERE player_scores.id = OLD.winner;

          UPDATE player_scores SET
              loses = (SELECT count(*) FROM matches WHERE matches.loser = player_scores.id LIMIT 1)
          WHERE player_scores.id = OLD.loser
          ;

          RETURN OLD;

      END IF;
      RETURN NULL;
  END;
  $$ LANGUAGE plpgsql;

CREATE TRIGGER update_scores_wrt_match AFTER INSERT OR DELETE
  ON matches
  FOR EACH ROW
  EXECUTE PROCEDURE update_scores_wrt_match_func();
