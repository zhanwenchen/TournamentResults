# TournamentResults
### A console database app to play Swiss-style chess tournaments

## Instructions

1. Set up PostgreSQL schema

  In bash, navigate to project folder, run

  ```
  $ psql
  ```
  which gets you inside the PostgreSQL console.

  Then import the tournament.sql script which creates the database, its tables,
  triggers, and its procedures.

  ```
  psql=> \i tournament.sql
  ```

  After the setting up is complete, quit the PostgreSQL console by

  ```
  psql=> \q
  ```

2. Run Python code (tests)

  To see this app in action, in bash run

  ```
  $ python tournament_test.py
  ```

  After which you can see the test results
