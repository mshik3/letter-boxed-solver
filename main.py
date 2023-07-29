import copy


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root

        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return self.output


## Create a dictionary trie that contains all words that are possible with the given input
## Given the inputted characters, cycle through all possible words that begin with each character
## and contain only the characters given. Add those to the trie

entire_dictionary_trie = Trie()

wordlist = [line.strip() for line in open("word_list.txt")]

for word in wordlist:
    entire_dictionary_trie.insert(word)

inp = input("What are the letters given? Separate them by a space: ")

sides = inp.split(" ")

all_chars = set()
for side in sides:
    for char in side:
        all_chars.add(char)

all_possible_words_trie = Trie()

for c in all_chars:
    possible_words = entire_dictionary_trie.query(c)
    for w in possible_words:
        w_set = set(w)
        if w_set.issubset(all_chars):
            all_possible_words_trie.insert(w)

## Find word that reduces remaining character list as much as possible.
## choose that word
## remove all chars used from the remaining character list
## repeat


def count_used_characters(word, char_set):
    word_set = set(word)
    char_set = set(char_set)

    return len(word_set.intersection(char_set))


# for side_index in range(4):
#     for l_index in range(3):
#         side = sides[side_index]
#         l = side[l_index]

#         other_sides = [s for s in sides if s != side]
#         word_using_max_characters = ""
#         for other_side in other_sides:
#             for second_character in other_side:
#                 prefix = str(l+second_character)


def is_valid_word(word, list_of_lists):
    if len(word) < 3:
        return False
    current_set = None
    for char in word:
        found_in_set = False
        for char_set in list_of_lists:
            if char in char_set:
                if current_set is None or current_set != char_set:
                    current_set = char_set
                    found_in_set = True
                    break
        if not found_in_set:
            return False
    return True


all_valid_words_trie = Trie()

for c in all_chars:
    c_words = all_possible_words_trie.query(c)
    for word in c_words:
        if is_valid_word(word, sides):
            all_valid_words_trie.insert(word)


chain = []


def recurse(letter, chain, characters_left):
    if len(chain) > 6:
        return chain

    if len(characters_left) == 0:
        return chain

    valid_words = all_valid_words_trie.query(letter)
    try:
        word_using_most_characters = valid_words[0]
    except Exception:
        print(f"skipping {letter}, there are no valid words for it")
        return chain
    most_characters_used = count_used_characters(
        word_using_most_characters, characters_left
    )
    for word in valid_words:
        used_characters = count_used_characters(word, characters_left)
        if used_characters > most_characters_used:
            word_using_most_characters = word
            most_characters_used = used_characters

    chain.append(word_using_most_characters)
    characters_left.difference_update(set(word_using_most_characters))

    return recurse(word_using_most_characters[-1], chain, characters_left)


chains = []
for start in all_chars:
    characters_left = copy.deepcopy(all_chars)
    chain = recurse(start, [], characters_left)
    chains.append(chain)

print(chains)
print(min(chains, key=len))
