"""Simple validation script for HW1 'friends'"""

# Note that fulfilling all of these requirements does NOT guarantee a fully correct implementation

from py_friends.friends import Friends
import myfriends
import pytest
import copy

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


def test_load_pairs_skips_empty_and_strips_whitespace(tmp_path):
    # Mix of blank lines, leading/trailing spaces, and tabs
    content = (
        "  CHEWBACCA   R2-D2  \n"  # leading/trailing + multiple spaces
        "\n"  # empty line -> should be skipped
        "C-3PO    R2-D2\n"  # multiple spaces
        "\tLUKE\tR2-D2\t\n"  # tabs
    )
    f = tmp_path / "friends_ws.txt"
    f.write_text(content, encoding="utf-8")

    pairs = myfriends.load_pairs(str(f))
    assert pairs == [
        ("CHEWBACCA", "R2-D2"),
        ("C-3PO", "R2-D2"),
        ("LUKE", "R2-D2"),
    ], "Should split on any whitespace, trim around lines, and skip empty ones"


def test_load_pairs_preserves_duplicates_and_order(tmp_path):
    # Duplicates must be preserved, and order must match file order
    content = (
        "HAN LEIA\n"
        "HAN LEIA\n"  # duplicate
        "LEIA HAN\n"  # reversed order is a distinct tuple at this stage
    )
    f = tmp_path / "friends_dups.txt"
    f.write_text(content, encoding="utf-8")

    pairs = myfriends.load_pairs(str(f))
    assert pairs == [
        ("HAN", "LEIA"),
        ("HAN", "LEIA"),
        ("LEIA", "HAN"),
    ], "Duplicates and input order should be preserved by load_pairs()"


def test_load_pairs_keeps_self_pairs(tmp_path):
    # Self-pairs are NOT filtered here (filtering happens in make_friends_directory)
    content = (
        "A A\n"
        "B A\n"
    )
    f = tmp_path / "friends_self.txt"
    f.write_text(content, encoding="utf-8")

    pairs = myfriends.load_pairs(str(f))
    assert pairs == [("A", "A"), ("B", "A")], "Self-pairs must be kept in raw list"


def test_load_pairs_ignores_malformed_single_token_lines(tmp_path):
    # Defensive behavior: skip lines that don't have at least two tokens
    content = (
        "HAN\n"  # malformed: single token -> should be skipped
        "\n"  # empty -> skipped
        "LEIA HAN\n"  # valid
        "  \t  \n"  # whitespace only -> skipped
    )
    f = tmp_path / "friends_malformed.txt"
    f.write_text(content, encoding="utf-8")

    pairs = myfriends.load_pairs(str(f))
    assert pairs == [("LEIA", "HAN")], "Lines with < 2 tokens should be ignored"


def test_load_pairs_handles_mixed_whitespace_and_crlf(tmp_path):
    # Simulate Windows CRLF and mixed whitespace between names
    content = "OBI-WAN   R2-D2\r\nBERU\t\tOWEN\r\n"
    f = tmp_path / "friends_crlf.txt"
    f.write_text(content, encoding="utf-8")

    pairs = myfriends.load_pairs(str(f))
    assert pairs == [("OBI-WAN", "R2-D2"), ("BERU", "OWEN")]


simple_pairs = [('CHEWBACCA', 'HAN'), ('CHEWBACCA', 'LUKE'), ('HAN', 'LEIA')]
simple_dir = {'CHEWBACCA': {'HAN', 'LUKE'}, 'HAN': {'CHEWBACCA', 'LEIA'},
              'LUKE': {'CHEWBACCA'}, 'LEIA': {'HAN'}}


def test_make_friends_directory_simple():
    """Test that keys and values are correctly made in small dictionary"""
    comment = "function did not return the correct directory"

    my_dir = myfriends.make_friends_directory(simple_pairs)
    assert my_dir == simple_dir, comment


def _assert_undirected_and_self_free(d):
    """Helper: every edge is reciprocal and no self-edges exist."""
    for u, nbrs in d.items():
        assert isinstance(nbrs, set), "Each value must be a set of friends"
        assert u not in nbrs, f"Self relationship should not appear: {u}"
        for v in nbrs:
            assert u in d.get(v, set()), f"Missing reciprocal edge for ({u}, {v})"


def test_make_friends_directory_empty_input_returns_empty_dict():
    pairs = []
    d = myfriends.make_friends_directory(pairs)
    assert d == {}, "Empty input should produce an empty directory"


def test_make_friends_directory_basic_undirected():
    pairs = [('CHEWBACCA', 'HAN'),
             ('CHEWBACCA', 'LUKE'),
             ('HAN', 'LEIA')]
    expected = {
        'CHEWBACCA': {'HAN', 'LUKE'},
        'HAN': {'CHEWBACCA', 'LEIA'},
        'LUKE': {'CHEWBACCA'},
        'LEIA': {'HAN'}
    }
    d = myfriends.make_friends_directory(pairs)
    assert d == expected, "Should build correct undirected adjacency sets"
    _assert_undirected_and_self_free(d)


def test_make_friends_directory_includes_right_side_only_names():
    # 'B' only appears on the right side; it must still appear as a key.
    pairs = [('A', 'B')]
    d = myfriends.make_friends_directory(pairs)
    assert set(d.keys()) == {'A', 'B'}, "All mentioned names must be keys"
    assert d['A'] == {'B'} and d['B'] == {'A'}, "Undirected relationship must be reflected"
    _assert_undirected_and_self_free(d)


def test_make_friends_directory_ignores_self_pairs_only_self():
    # Only a self-pair should result in an empty directory
    pairs = [('X', 'X')]
    d = myfriends.make_friends_directory(pairs)
    assert d == {}, "Self-pairs must be ignored and not create keys"


def test_make_friends_directory_ignores_self_pairs_when_mixed():
    pairs = [('A', 'A'), ('A', 'B'), ('B', 'B'), ('B', 'C')]
    d = myfriends.make_friends_directory(pairs)
    assert set(d.keys()) == {'A', 'B', 'C'}
    assert d['A'] == {'B'}
    assert d['B'] == {'A', 'C'}
    assert d['C'] == {'B'}
    # Ensure no self-edges snuck in
    for k in d:
        assert k not in d[k], "No self-relationships should appear in sets"
    _assert_undirected_and_self_free(d)


def test_make_friends_directory_handles_duplicates_and_reverse_duplicates():
    # Multiple repeats and reversed inputs should collapse into a single undirected edge
    pairs = [('A', 'B'), ('A', 'B'), ('B', 'A'), ('A', 'B')]
    d = myfriends.make_friends_directory(pairs)
    assert set(d.keys()) == {'A', 'B'}
    assert d['A'] == {'B'} and d['B'] == {'A'}
    # Sets should have length 1 due to uniqueness
    assert len(d['A']) == 1 and len(d['B']) == 1
    _assert_undirected_and_self_free(d)


def test_make_friends_directory_value_types_are_sets():
    pairs = [('HAN', 'LEIA'), ('LEIA', 'LUKE')]
    d = myfriends.make_friends_directory(pairs)
    for val in d.values():
        assert isinstance(val, set), "Each dictionary value should be a set"
    _assert_undirected_and_self_free(d)


def test_make_friends_directory_multiple_components_ok():
    # Two disconnected components should both be represented correctly
    pairs = [('A', 'B'), ('C', 'D')]
    d = myfriends.make_friends_directory(pairs)
    assert d['A'] == {'B'}
    assert d['B'] == {'A'}
    assert d['C'] == {'D'}
    assert d['D'] == {'C'}
    _assert_undirected_and_self_free(d)


def test_returns_empty_list_on_empty_dir():
    assert myfriends.find_all_number_of_friends({}) == [], \
        "Empty directory should return an empty list"


def test_basic_counts_and_desc_sorting():
    # Mixed degrees: C:3, A:2, B:1 (unordered input)
    my_dir = {
        "A": {"B", "C"},
        "B": {"A"},
        "C": {"A", "B", "D"},
        "D": {"C"},  # D has 1, but not included as key alone in description—still valid here
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    # Expected sorted by (-count, name)
    expected = [
        ("C", 3),
        ("A", 2),
        ("B", 1),
        ("D", 1),
    ]
    assert got == expected


def test_tie_break_ascii_order_when_counts_equal():
    # All have exactly 2 friends; check ASCII tie-break by name
    my_dir = {
        "CHEWBACCA": {"HAN", "LUKE"},
        "HAN": {"CHEWBACCA", "LEIA"},
        "LEIA": {"HAN", "LUKE"},
        "LUKE": {"CHEWBACCA", "LEIA"},
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    expected = [
        ("CHEWBACCA", 2),
        ("HAN", 2),
        ("LEIA", 2),
        ("LUKE", 2),
    ]  # Already ASCII by key
    assert got == expected, "When counts tie, names must be ASCII-sorted"


def test_includes_zero_friend_people_and_places_them_last_by_count():
    # 'LONER' has 0 friends and should appear after those with >0 friends.
    my_dir = {
        "HAN": {"LEIA"},
        "LEIA": {"HAN"},
        "LONER": set(),
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    expected = [
        ("HAN", 1),
        ("LEIA", 1),  # tie at 1 -> ASCII 'HAN' < 'LEIA'
        ("LONER", 0),  # zeros come last
    ]
    assert got == expected


def test_non_mutation_of_input_directory():
    my_dir = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"},
    }
    before = copy.deepcopy(my_dir)
    _ = myfriends.find_all_number_of_friends(my_dir)
    assert my_dir == before, "Function should not mutate the input directory"


def test_ascii_order_with_punctuation_and_digits_in_names():
    # Same degree for all; enforce ASCII order: 'A' < 'B' < 'R2-1' < 'R2-D2'
    my_dir = {
        "R2-D2": {"X", "Y"},
        "R2-1": {"X", "Y"},
        "A": {"X", "Y"},
        "B": {"X", "Y"},
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    expected = [
        ("A", 2),
        ("B", 2),
        ("R2-1", 2),
        ("R2-D2", 2),
    ]
    assert got == expected, "Tie-break should follow ASCII order across punctuation/digits"


def test_case_sensitivity_ascii_order_upper_before_lower_on_tie():
    # Python string order places 'A' (65) before 'a' (97)
    my_dir = {
        "alpha": {"x", "y"},
        "ALPHA": {"x", "y"},
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    expected = [("ALPHA", 2), ("alpha", 2)]
    assert got == expected, "Uppercase should come before lowercase in ASCII order on ties"


def test_unreciprocated_edges_still_count_sizes_of_sets():
    # Counts are based on set sizes, not verifying symmetry
    my_dir = {
        "X": {"Y"},
        "Y": set(),  # Y lists no one, should count as 0
    }
    got = myfriends.find_all_number_of_friends(my_dir)
    expected = [("X", 1), ("Y", 0)]
    assert got == expected


def test_insertion_order_of_dict_does_not_affect_result():
    my_dir1 = {
        "C": {"A"},
        "A": {"B"},
        "B": {"A", "C"},
    }
    # Different insertion order
    my_dir2 = {}
    my_dir2["A"] = {"B"}
    my_dir2["B"] = {"A", "C"}
    my_dir2["C"] = {"A"}

    got1 = myfriends.find_all_number_of_friends(my_dir1)
    got2 = myfriends.find_all_number_of_friends(my_dir2)
    assert got1 == got2 == [("B", 2), ("A", 1), ("C", 1)]


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


def test_roster_matches_spec_example():
    # From the assignment handout
    my_dir = {
        'CHEWBACCA': {'HAN', 'LUKE'},
        'HAN': {'CHEWBACCA', 'LEIA'},
        'LUKE': {'CHEWBACCA'},
        'LEIA': {'HAN'}
    }
    assert myfriends.make_team_roster('HAN', my_dir) == 'HAN_CHEWBACCA_LEIA_LUKE'


def test_two_hops_only_chain_no_spillover_to_third_hop():
    # A - B - C - D
    my_dir = {
        'A': {'B'},
        'B': {'A', 'C'},
        'C': {'B', 'D'},
        'D': {'C'},
    }
    # For A: direct {B}; FoF includes {C}; NOT D (third hop)
    assert myfriends.make_team_roster('A', my_dir) == 'A_B_C'
    # For B: direct {A, C}; FoF adds {D} (from C), not adding B itself
    assert myfriends.make_team_roster('B', my_dir) == 'B_A_C_D'


def test_no_friends_returns_leader_only():
    my_dir = {
        'LONER': set(),
    }
    assert myfriends.make_team_roster('LONER', my_dir) == 'LONER'


def test_ascii_order_and_deduplication_of_direct_and_fof():
    # Mixed case to exercise ASCII ordering (uppercase before lowercase)
    # Direct: 'B', 'b'; FoF adds 'Y' (from 'B') and 'Z' (from 'b')
    my_dir = {
        'A': {'B', 'b'},
        'B': {'A', 'Y'},
        'b': {'A', 'Z'},
        'Y': set(),
        'Z': set(),
    }
    # ASCII order: 'B' < 'Y' < 'Z' < 'b'
    assert myfriends.make_team_roster('A', my_dir) == 'A_B_Y_Z_b'


def test_excludes_leader_from_tail_even_if_present_via_self_edge():
    # Although make_friends_directory avoids self-edges, ensure robustness
    my_dir = {
        'SELF': {'SELF', 'X'},
        'X': {'SELF'},
    }
    # 'SELF' must not appear after the first token
    assert myfriends.make_team_roster('SELF', my_dir) == 'SELF_X'


def test_missing_friend_key_in_directory_is_safe():
    # 'X' is a direct friend but missing as a key; get() should handle it.
    my_dir = {
        'A': {'X'},  # 'X' not present as a key
    }
    assert myfriends.make_team_roster('A', my_dir) == 'A_X'


def test_assertion_on_unknown_leader():
    my_dir = {'A': {'B'}, 'B': {'A'}}
    with pytest.raises(AssertionError):
        myfriends.make_team_roster('GHOST', my_dir)


def test_cycles_dont_duplicate_and_respect_two_hops():
    # Triangle A-B-C-A and an extra tail C-D
    my_dir = {
        'A': {'B', 'C'},
        'B': {'A', 'C'},
        'C': {'A', 'B', 'D'},
        'D': {'C'},
    }
    # For A: direct {B,C}; FoF from B and C adds {A, C} and {A, B, D} -> adds only D uniquely
    # ASCII: 'B', 'C', 'D'
    assert myfriends.make_team_roster('A', my_dir) == 'A_B_C_D'


def test_non_mutation_of_input_directory():
    my_dir = {
        'A': {'B', 'C'},
        'B': {'A'},
        'C': {'A'},
    }
    before = copy.deepcopy(my_dir)
    _ = myfriends.make_team_roster('A', my_dir)
    assert my_dir == before, "make_team_roster should not mutate the input directory"


def test_ascii_order_with_digits_and_punctuation():
    # Ensure ASCII sort is used for tie-breaking among team members
    my_dir = {
        'R2-D2': {'C3PO', 'OBI-WAN', 'LUKE'},
        'C3PO': {'R2-D2'},
        'OBI-WAN': {'R2-D2'},
        'LUKE': {'R2-D2'},
    }
    # Team members: C3PO, LUKE, OBI-WAN; ASCII order: 'C3PO' < 'LUKE' < 'OBI-WAN'
    assert myfriends.make_team_roster('R2-D2', my_dir) == 'R2-D2_C3PO_LUKE_OBI-WAN'


simple_team = 'LEIA_CHEWBACCA_HAN'


def test_find_smallest_team_simple():
    """Test that team found and str correctly returned"""
    comment = "function did not return correct underscore-separated str"

    my_team = myfriends.find_smallest_team(simple_dir)
    assert my_team == simple_team, comment


def test_empty_directory_returns_empty_string():
    assert myfriends.find_smallest_team({}) == "", \
        "Empty directory should return an empty string"


def test_single_isolated_person_returns_just_leader():
    my_dir = {"A": set()}
    assert myfriends.find_smallest_team(my_dir) == "A"


def test_multiple_isolated_people_tie_breaks_by_ascii_label():
    # All teams have size 0 -> labels are just the leader names
    my_dir = {"B": set(), "A": set(), "C": set()}
    # ASCII order: "A" < "B" < "C"
    assert myfriends.find_smallest_team(my_dir) == "A"


def test_prefers_smaller_team_over_larger_even_if_label_ascii_is_bigger():
    # 'B' is isolated (team size 0), 'A' has two teammates (size 2).
    my_dir = {
        "A": {"C", "D"},
        "C": {"A"},
        "D": {"A"},
        "B": set(),
    }
    assert myfriends.find_smallest_team(my_dir) == "B"


def test_chain_graph_two_hops_only_no_third_hop():
    # A - B - C - D
    my_dir = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B", "D"},
        "D": {"C"},
    }
    # A's team: {B, C} (no D), size 2 -> label "A_B_C"
    # D's team: {B, C}, size 2 -> label "D_B_C"
    # Tie on size -> pick ASCII-min label across full roster strings
    assert myfriends.find_smallest_team(my_dir) == "A_B_C"


def test_tie_break_on_equal_sizes_uses_full_label_ascii_order():
    # Two separate pairs with size-1 teams; tie broken by roster label.
    my_dir = {
        "ALPHA": {"B"},
        "B": {"ALPHA"},
        "BETA": {"A"},
        "A": {"BETA"},
    }
    # Labels: "ALPHA_B" and "BETA_A" (both size 1) -> ASCII "ALPHA_B" first
    assert myfriends.find_smallest_team(my_dir) == "ALPHA_B"


def test_robust_when_friend_key_is_missing():
    # 'X' is a friend of 'A' but is not a key in the directory
    my_dir = {
        "A": {"X"},
        "B": {"C"},
        "C": {"B"},
        # no "X" key
    }
    # A's team: {'X'} -> "A_X" (size 1)
    # B's team: {'C'} -> "B_C" (size 1)
    # Tie -> ASCII: "A_X" < "B_C"
    assert myfriends.find_smallest_team(my_dir) == "A_X"


def test_digits_and_punctuation_in_ascii_tie_break():
    my_dir = {
        "R2-D2": {"LUKE"},
        "R2-1": {"LUKE"},
        "LUKE": {"R2-D2", "R2-1"},
    }
    assert myfriends.find_smallest_team(my_dir) == "LUKE_R2-1_R2-D2"


def test_cycle_plus_tail_picks_true_min_size_then_ascii():
    # Triangle A-B-C-A and extra tail C-D
    my_dir = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B", "D"},
        "D": {"C"},
    }
    assert myfriends.find_smallest_team(my_dir) == "A_B_C_D"


def test_does_not_mutate_input_directory():
    my_dir = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"},
    }
    before = copy.deepcopy(my_dir)
    _ = myfriends.find_smallest_team(my_dir)
    assert my_dir == before, "find_smallest_team must not mutate the input directory"


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


def test_empty_directory_yields_nothing():
    # Catches the bad empty init (self.person vs self.persons)
    it = Friends({})
    assert list(it) == [], "Empty directory should iterate to no pairs"


def test_basic_triangle_unique_and_sorted():
    # Complete triangle; should yield each unique pair once in ASCII order
    d = {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"},
    }
    got = list(Friends(d))
    assert got == [("A", "B"), ("A", "C"), ("B", "C")]


def test_first_person_self_edge_is_ignored_and_no_reverse_pair():
    # First key in ASCII is 'A'; includes self 'A' and friend 'B'
    # This catches missing s > person filter in __init__
    d = {
        "B": {"A"},  # ensure more than one key
        "A": {"A", "B"},  # 'A' self-edge should not appear
    }
    got = list(Friends(d))
    assert got == [("A", "B")], "Must not emit ('A','A') nor ('B','A')"


def test_within_person_ascii_order_not_reversed():
    # Catches the pop() vs pop(0) bug: should emit ('A','B') then ('A','C')
    d = {
        "A": {"C", "B"},
        "B": {"A"},
        "C": {"A"},
    }
    got = list(Friends(d))
    assert got == [("A", "B"), ("A", "C")], "Pairs within a person must be ASC by friend"


def test_across_persons_ascii_block_order():
    # All 'A' pairs first, then 'B' pairs, etc.
    d = {
        "B": {"C"},  # ensure 'B' appears
        "A": {"B", "C"},
        "C": {"A", "B"},
    }
    got = list(Friends(d))
    assert got == [("A", "B"), ("A", "C"), ("B", "C")]


def test_missing_friend_key_still_emits_pair():
    # Friend exists in A's set but not as a directory key; still should yield
    d = {"A": {"X"}}
    got = list(Friends(d))
    assert got == [("A", "X")]


def test_self_edges_anywhere_never_emitted():
    d = {
        "A": {"A"},  # self only
        "B": {"B", "C"},  # plus a valid friend
        "C": {"B"},
    }
    got = list(Friends(d))
    assert got == [("B", "C")], "Self-pairs must never appear"


def test_iterator_protocol_and_stopiteration():
    d = {"A": {"B"}, "B": {"A"}}
    it = Friends(d)
    # __iter__ returns self
    assert iter(it) is it
    # next works and then raises StopIteration
    assert next(it) == ("A", "B")
    with pytest.raises(StopIteration):
        next(it)


def test_yields_tuples_not_lists():
    d = {"A": {"B"}, "B": {"A"}}
    out = list(Friends(d))
    assert all(isinstance(p, tuple) and len(p) == 2 for p in out)


def test_does_not_mutate_input_directory():
    d = {
        "A": {"B", "C"},
        "B": {"A"},
        "C": {"A"},
    }
    before = copy.deepcopy(d)
    _ = list(Friends(d))
    assert d == before, "Iterator must not mutate the source directory"