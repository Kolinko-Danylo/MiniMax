from binary_search_tree.linkedbst import LinkedBST
import random
from string import ascii_lowercase as low
import time

dictionary = [("".join([random.choice(low) for i in range(random.randint(2, 11))])) for j in range(10 ** 5)]

def test_time_list(lst):
    start = time.time()
    for i in range(10**4):
        word = random.choice(lst)
        j = 0
        while lst[j] != word:
            j += 1
    return time.time() - start


def test_bst(lst):
    bst = LinkedBST()
    for i in lst:
        bst.add(i)
    start = time.time()
    for i in range(10 ** 4):
        word = random.choice(lst)
        word1 = bst.find(word)
        assert word == word1
    return time.time() - start

def test_balanced_bst(lst):
    bst = LinkedBST()
    for i in lst:
        bst.add(i)
    bst.rebalance()
    start = time.time()
    for i in range(10 ** 4):
        word = random.choice(lst)
        word1 = bst.find(word)
        assert word == word1
    return time.time() - start


print(test_time_list(dictionary))
print(test_bst(dictionary))
print(test_balanced_bst(dictionary))