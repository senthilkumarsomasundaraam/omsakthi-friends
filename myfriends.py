"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions,
  including testing of "edge cases"
"""

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: oea497
Groupmate 2: ltq85
"""


def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

        # ------------ BEGIN YOUR CODE ------------
        for line in infile:
            res = line.split()
            if len(res) != 2: continue
            if res is None: continue
            list_of_pairs.append((res[0].strip(), res[1].strip()))

    # ------------ END YOUR CODE ------------
    # Changed Pass to continue
    # Changed split("") to split so it avoids empty strings and recognizes other empty space types like /t
    # Implemented a skip if a line has more than or less than 2 names
    #
    #

    return list_of_pairs


def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way:
      if given a pair (x,y), then assume that y is a friend of x, and x is
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    # ------------ BEGIN YOUR CODE ------------
    for i in pairs:
        if len(i) != 2: continue  # Add this to make sure that the input is
        if i[0] == i[1]: continue  # Ignore duplicated pair first.
        if i[0] not in directory:
            directory[i[0]] = set()

        # First I will check if the person is already listed
        if i[1] not in directory:
            directory[i[1]] = set()

        directory[i[0]].add(i[1])  # Add the second person the friend to the friend list
        directory[i[1]].add(i[0])  # Do the opposite,  Add the first person the friend to second friend list

    # pass    # implement your code here

    # ------------ END YOUR CODE ------------
    # 1 Added a clause to ignore cases like [(a,a)]

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list
    of 2-tuples, where each tuples has the person's name as the first element,
    the the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------
    for i in my_dir:
        host_name = i
        friends_num = len(my_dir[i])
        friends_list.append((host_name, friends_num))

    ### First we first sort by the secondary key, the name
    friends_list = sorted(friends_list, key=lambda i: i[0], reverse=False)
    ### Now we first sort by the first key, the figure
    friends_list = sorted(friends_list, key=lambda i: i[1], reverse=True)

    # ------------ END YOUR CODE ------------
    # Reviewed, no changes, no notes

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the
        team leader's name, i.e. A.  Subsequent unique substrings are
        friends of A or friends of friends of A, in ASCII order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------
    friends_level_1 = my_dir[person]

    friends_set = set(friends_level_1)
    # friends_set |= set(person)

    friends_level_2 = set()
    for i in friends_level_1:
        if i not in my_dir: continue  # 1
        friends_level_2 |= set(my_dir[i])

    friends_set |= friends_level_2
    friends_set.discard(person)  # Just in case

    for i in sorted(friends_set):
        if i != person: label = label + "_" + i

    # ------------ END YOUR CODE ------------
    # Deleted pass statement
    # 1 Added instruction to skip adding the friends of a friend if that person has no friends registered

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ASCII order
    """
    smallest_teams = []
    # last_team_roster = str()
    # ------------ BEGIN YOUR CODE
    for i in my_dir:
        temp_list = make_team_roster(i, my_dir)
        if len(smallest_teams) == 0:
            smallest_teams = temp_list

        if len(smallest_teams.split('_')) > len(temp_list.split('_')):
            smallest_teams = temp_list

        elif len(smallest_teams.split('_')) == len(temp_list.split('_')):

            if temp_list < smallest_teams:
                smallest_teams = temp_list
    if type(smallest_teams) is not type([]):
        smallest_teams = [smallest_teams]

    # ------------ END YOUR CODE
    # Added a conditional in "smallest_teams = [smallest_teams]" so empty dictionaries return "" properly

    return smallest_teams[0] if smallest_teams else ""


def generate_friends(friends_dict):
    if type(friends_dict) is not dict: return None
    ### I am going to loop through each key and name then create the tuple

    persons_list = sorted(friends_dict.keys())
    completed_person = set()
    for person in persons_list:
        for friend in sorted(friends_dict[person]):
            if friend not in completed_person:
                yield person, friend
        completed_person.add(person)


if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('myfriends.txt')
    print(my_pairs)

    print('\n2. run make_friends_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir)

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))

    print('\n4. run make_team_roster')
    my_person = 'DARTHVADER'  # test with this person as team leader
    team_roster = make_team_roster(my_person, my_dir)
    print(f"team_roster of {my_person} is {team_roster}")

    my_person = 'HAN'  # test with this person as team leader
    print(f"team_roster of {my_person} is {make_team_roster(my_person, my_dir)}")

    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        # if num == 10:
        #     break
    # since index 0 we read 11 elements
    print(len(list(friends_iterator)) + num + 1)

    print('\n7. run the Generator Friends iterator')
    generated_friends = generate_friends(my_dir)
    for num, pair in enumerate(generated_friends):
        print(num, pair)
        # if num == 10:
        #     break
    # since index 0 we read 11 elements
    print(len(list(generated_friends)) + num + 1)



