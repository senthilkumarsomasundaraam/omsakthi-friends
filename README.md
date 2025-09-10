# DSC 395T – Algorithms and Data Structures Programming Assignment #1: Friend of a Friend Group Project

This project practices Python sequence types (list, dict, tuple, set, str) and programming constructs by analyzing a dataset of friendship relations (pairs of #characters appearing together in Star Wars scenes). Only the Python standard library and pytest may be used.

#Tasks
Load Pairs
Implement load_pairs() to read a text file of friendship pairs.
Returns a list of 2-tuples (may include duplicates).
Friendship Directory
Implement make_friends_directory() to convert the list of tuples into a dictionary.
Keys = person, Values = set of that person’s friends.
Friendships are bidirectional, and self-pairs (x, x) are ignored.
Friend Counts
Implement find_all_number_of_friends() to return a sorted list of (person, number_of_friends).
Sorted by descending number of friends, ties broken by ASCII order.
Team Roster
Implement make_team_roster() to compute a person’s team = friends + friends-of-friends.
Return a team roster string (names joined with _).
Smallest Team

Implement find_smallest_team() to return the roster string of the smallest team.
If tied, return ASCII-order first.
Iterator Class

Fix the provided Friends class (py_friends/friends.py) to correctly iterate (ASCII order) over unique friendship relations.
Optional Karma

Implement generate_friends() (a generator) that replicates the iterator functionality.

#Testing

Run tests with:
pytest tests/test_friends.py::test_load_pairs_simple
