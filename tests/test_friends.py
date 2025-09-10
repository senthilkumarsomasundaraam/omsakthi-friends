"""Simple validation script for HW1 'friends'"""

# Note that fulfilling all of these requirements does NOT guarantee a fully correct implementation

from py_friends.friends import Friends
import myfriends
import pytest

# Expected solutions from a simplified test example
simple_file = 'myfriends.txt'
simple_file_len = 58
comment_length = "function returned list of incorrect length"

def test_load_pairs_simple():
    """Test that list of correct length returned. Does not check list contents"""

    comment = "function's return type should be a list"

    my_pairs = myfriends.load_pairs(simple_file)
    assert isinstance(my_pairs, list), comment
    assert len(my_pairs) == simple_file_len, comment_length


simple_pairs = [('CHEWBACCA', 'HAN'), ('CHEWBACCA', 'LUKE'), ('HAN', 'LEIA')]
simple_dir = {'CHEWBACCA': {'HAN', 'LUKE'}, 'HAN': {'CHEWBACCA', 'LEIA'}, 
                'LUKE': {'CHEWBACCA'}, 'LEIA': {'HAN'}}

def test_make_friends_directory_simple():
    """Test that keys and values are correctly made in small dictionary"""
    comment = "function did not return the correct directory"

    my_dir = myfriends.make_friends_directory(simple_pairs)
    assert my_dir == simple_dir, comment


simple_friends = [('CHEWBACCA', 2), ('HAN', 2), ('LEIA', 1), ('LUKE', 1)]

def test_find_all_number_of_friends_simple():
    """Test that numbers of friends found are correct"""
    comment = "function did not return correct list of tuples"

    my_friends = myfriends.find_all_number_of_friends(simple_dir)
    assert len(my_friends) == len(simple_friends), comment_length
    assert all([f in my_friends for f in simple_friends]), comment


simple_person = 'HAN'
simple_roster = 'HAN_CHEWBACCA_LEIA_LUKE'

def test_make_team_roster_simple():
    """Test that correct team roster str returned"""
    comment = "function did not return correct underscore-separated str"

    my_roster = myfriends.make_team_roster(simple_person, simple_dir)
    assert my_roster == simple_roster, comment


simple_team = 'LEIA_CHEWBACCA_HAN'

def test_find_smallest_team_simple():
    """Test that team found and str correctly returned"""
    comment = "function did not return correct underscore-separated str"

    my_team = myfriends.find_smallest_team(simple_dir)
    assert my_team == simple_team, comment


simple_first = ('CHEWBACCA', 'HAN')

def test_Friends_simple():
    """Test that the iterator returns correct first element"""

    comment = "iterator did not return correct first str"

    myFriends = myfriends.Friends(simple_dir)
    my_iterator = myFriends.__iter__()
    my_first = my_iterator.__next__()
    assert my_first == simple_first, comment
    

simple_iter_len = 3

def test_Friends_length_simple():
    """Test that the iterator returns correct number of elements"""

    comment = "did not iterate over correct number of elements"

    myFriends = Friends(simple_dir)
    assert len(list(myFriends)) == simple_iter_len, comment

