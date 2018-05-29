class Tree:
    """Simple representation of Tree data structure"""

    def __init__(self, root=None):
        self._root = root

    def get_root(self):
        return self._root

    def set_rootValue(self, value):
        self._root = value


class Node:
    "Represent node in tree"

    def __init__(self, data):
        self.children = []
        self.data = data
        self.score = 0
