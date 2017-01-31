#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


# Connect to the PostgreSQL database.  Returns a database connection.
def connect():
    return psycopg2.connect("dbname=tournament")


# Remove all the match records from the database.
def deleteMatches():
    DELETE_MATCHES_QUERY = "DELETE FROM matches"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(DELETE_MATCHES_QUERY)
    connection.commit()
    connection.close()

# Remove all the player records from the database.
def deletePlayers():
    DELETE_PLAYERS_QUERY = "DELETE FROM players"

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(DELETE_PLAYERS_QUERY)

    connection.commit()
    connection.close()

# Returns the number of players currently registered.
# Example
def countPlayers():
    COUNT_PLAYERS_QUERY = "SELECT count(*) FROM players"

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(COUNT_PLAYERS_QUERY)

    count = cursor.fetchall()[0][0]
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

    REGISTER_PLAYERS_QUERY = """INSERT INTO players (name) VALUES (%s);"""

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(REGISTER_PLAYERS_QUERY, (name,))

    connection.commit()
    connection.close()

# def updateScores():
#     UPDATE_SCORES_QUERY = """
#         UPDATE players
#             SET wins =
#                 (SELECT count(*)
#                     FROM matches
#                     WHERE winner = %s
#                     LIMIT 1
#                 )
#             WHERE id = %s;
#
#         UPDATE players
#             SET loses =
#                 (SELECT count(*)
#                     FROM matches
#                     WHERE loser = %s
#                     LIMIT 1
#                 )
#             WHERE id = %s;
#     """
#     connection = connect()
#     cursor = connection.cursor()
#
#     cursor.execute(UPDATE_WINNER_QUERY, (winner, winner,))
#     cursor.execute(UPDATE_LOSER_QUERY, (loser, loser,))
#
#     connection.commit()
#     connection.close()


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
        SELECT id, name, wins, wins + loses as matches
        FROM players
        ORDER BY wins
        DESC
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(QUERY)
    player_standings = cursor.fetchall()
    connection.close()
    # print("\n\nplayer_standings is %s\n\n" % player_standings)
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    ADD_MATCH_QUERY = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(ADD_MATCH_QUERY, (winner,loser,))

    connection.commit()
    connection.close()

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
    # Each player is paired with another
    # player with an equal or nearly-equal win record, that is, a player adjacent
    # to him or her in the standings.

    # or use subselects or left joins
    SWISS_QUERY = """
        SELECT a.id, a.name, a.wins, b.id, b.name, b.wins
        FROM players AS a, players AS b
        WHERE a.wins = b.wins
            AND a.id < b.id
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(SWISS_QUERY)
    next_pairs = cursor.fetchall()
    print(next_pairs)
    connection.close()
    return next_pairs
