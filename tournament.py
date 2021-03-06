# tournament.py
#
#
# Functions definitions
# !/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


# Connect to the PostgreSQL database.
def connect(database_name="tournament"):
    try:
        connection = psycopg2.connect("dbname={}".format(database_name))
        cursor = connection.cursor()
        return connection, cursor
    except:
        print("Connection error in connect()")

# wrapper for queries not requiring a cursor returned
def queryWrapper(query, param=None):
    connection, cursor = connect()

    cursor.execute(query, param)
    connection.commit()
    connection.close()

# Remove all the match records from the database.
def deleteMatches():
    DELETE_MATCHES_QUERY = "DELETE FROM matches"
    queryWrapper(DELETE_MATCHES_QUERY)

# Remove all the player records from the database.
def deletePlayers():
    DELETE_PLAYERS_QUERY = "DELETE FROM player_names"
    queryWrapper(DELETE_PLAYERS_QUERY)

# Returns the number of players currently registered.
def countPlayers():
    COUNT_PLAYERS_QUERY = "SELECT count(*) FROM player_names;"

    connection, cursor = connect()
    cursor.execute(COUNT_PLAYERS_QUERY)

    count = cursor.fetchone()[0]
    connection.close()
    return count


# Adds a player to the tournament database.
#
# The database assigns a unique serial id number for the player.  (This
# should be handled by your SQL database schema, not in your Python code.)
#
# Args:
#   name: the player's full name (need not be unique).
# """
def registerPlayer(name):

    REGISTER_PLAYERS_QUERY = """INSERT INTO player_names (name) VALUES (%s);"""
    REGISTER_PLAYERS_PARAMS = (name,) # singleton tuple to prevent SQL injections

    queryWrapper(REGISTER_PLAYERS_QUERY, REGISTER_PLAYERS_PARAMS)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    QUERY = """
        SELECT
            player_names.id,
            player_names.name,
            player_scores.wins,
            player_scores.wins + player_scores.loses as matches
        FROM
            player_names,
            player_scores
        WHERE
            player_names.id = player_scores.id
        ORDER BY wins DESC
    """

    connection, cursor = connect()
    cursor.execute(QUERY)
    player_standings = cursor.fetchall()
    connection.close()
    # print(player_standings)
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    ADD_MATCH_QUERY = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    ADD_MATCH_PARAMS = (winner,loser,) # Two-tuple to prevent SQL injections

    queryWrapper(ADD_MATCH_QUERY, ADD_MATCH_PARAMS)

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    ## Use SQL JOIN to get unique combinations
    SWISS_QUERY = """
        SELECT
            a.id, c.name, b.id, c.name
        FROM
            player_scores AS a,
            player_scores AS b,
            player_names AS c,
            player_names AS d
        WHERE
            a.wins = b.wins
            AND a.id < b.id
            AND a.id = c.id
            AND b.id = d.id
    """

    connection, cursor = connect()
    cursor.execute(SWISS_QUERY)
    players = cursor.fetchall()
    # print(players)

    ## Use Python to filter out bidirectional duplicates
    next_pairs = []
    picked_players = []

    for [a_id, a_name, b_id, b_name] in players:
        # if a or b is already picked, skip
        if a_id in picked_players:
            continue
        if b_id in picked_players:
            continue

        # otherwise put them in picked_players
        picked_players.extend((a_id, b_id))
        next_pairs.append([a_id, a_name, b_id, b_name])
        # print(next_pairs)

    connection.close()
    return next_pairs
