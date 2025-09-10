
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
        # while line:
            res = line.split(' ')
            if res is None: pass
            list_of_pairs.append((res[0].strip(), res[1].strip()))
            pass    # implement your code here

# ------------ END YOUR CODE ------------

    return list_of_pairs


print('\n1. run load_pairs')
my_pairs = load_pairs('myfriends.txt')
print(my_pairs)

print(len(my_pairs))


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
        if i[0] not in directory:
            directory[i[0]] = set()  # Add the second person the friend to the friend list

        directory[i[0]].add(i[1])

    # Now I want to loop through it again to establish the two-way relationship.
    # First I will check if the person is already listed
        if i[1] not in directory:
            directory[i[1]] = set()  # Do the opposite,  Add the first person the friend to second friend list

        directory[i[1]].add(i[0])

    pass    # implement your code here


    # ------------ END YOUR CODE ------------

    return directory

dic = make_friends_directory(my_pairs)

print(dic)

print(len(dic['CHEWBACCA']))

for i in dic:
    print(f"{i}: {dic[i]}")

a = [(1 , 2), (2,3),(3,4)]
a.pop(0)