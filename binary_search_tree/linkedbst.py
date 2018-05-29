"""
File: linkedbst.py
Author: Ken Lambert
"""

from binary_search_tree.abstractcollection import AbstractCollection
from binary_search_tree.bstnode import BSTNode
from binary_search_tree.linkedstack import LinkedStack
from binary_search_tree.linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''

            if top is None:
                return 0
            amount = max(height1(top.left), height1(top.right))
            return amount + 1

        if self.isEmpty():
            return 0
        return height1(self._root) - 1

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''

        if (log(self._size + 1, 2) - 1 <= self.height()) and (self.height() <= log(self._size, 2)):
        #if (self.height()< 2*log(self._size+1)-1):
            return True
        return False

    def _tour(self):
        lst = []

        def node_tour(top, lst):
            if top.left is not None:
                lst = node_tour(top.left, lst)
            lst.append(top.data)
            if top.right is not None:
                lst = node_tour(top.right, lst)
            return lst

        lst = node_tour(self._root, lst)
        return lst

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        lst = []
        if self.find(low) is None:
            low = self.successor(low)
        if self.find(high) is None:
            high = self.predecessor(high)

        def node_tour(top, lst):
            if top.left is not None:
                lst = node_tour(top.left, lst)
            if low <= top.data and top.data <= high:
                lst.append(top.data)
            if top.right is not None:
                lst = node_tour(top.right, lst)
            return lst

        lst = node_tour(self._root, lst)

        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if self.isBalanced():
            return
        else:
            lst = self._tour()
            self.clear()

            def simple_add(lst):
                if not len(lst):
                    return
                first_part = lst[:len(lst) // 2]
                second_part = lst[len(lst) // 2 + 1:]
                self.add(lst[len(lst) // 2])
                simple_add(first_part)
                simple_add(second_part)

            simple_add(lst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self._tour()
        i = 0
        try:
            while item >= lst[i]:
                i += 1
        except IndexError:
            return

        return lst[i]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self._tour()
        i = -1
        try:
            while item <= lst[i]:
                i -= 1
        except IndexError:
            return

        return lst[i]

    def num_children(self, node):
        def recurse(node):
            if node is None:
                return 0
            else:
                return 1 + recurse(node.left) + recurse(node.right)
        return recurse(node) - 1
    def BFT_tree(self):
        current = self._root
        cur_queue = LinkedQueue()
        cur_queue.add(current)
        while not(cur_queue.isEmpty()):
            cur = cur_queue.pop()
            if cur is not None:
                cur_queue.add(cur.right)
                cur_queue.add(cur.left)
                print(cur.data)




if __name__ == "__main__":
    tree = LinkedBST()
    print("Adding D B A C F E G")
    tree.add("D")
    tree.add("B")
    tree.add("A")
    tree.add("C")
    tree.add("F")
    tree.add("E")
    tree.add("G")
    print("\nString:\n" + str(tree))
    print("balanced?", tree.isBalanced())
    print("Range find B-F:\n")
    print(tree.rangeFind("B", "F"))
    v91 = tree.num_children(tree._root.right)
    print(v91)
    tree = LinkedBST()
    for i in range(11):
        tree.add(i)
    print("\nString:\n" + str(tree))
    print("balanced?", tree.isBalanced())
    v91 = tree.num_children(tree._root.right)
    print(v91)
    tree.rebalance()
    print("balanced?", tree.isBalanced())
    print("\nString:\n" + str(tree))
    v91 = tree.num_children(tree._root.right)
    print(v91)
    tree = LinkedBST()
    for i in [113, 30, 68, 74, 45, 91, 88]:
        tree.add(i)
    print("\nString:\n" + str(tree))
    print(tree.isBalanced())
    v91 = tree.num_children(tree._root.right)
    print(v91)
    tree.rebalance()
    print("\nString:\n" + str(tree))
    print(tree.isBalanced())
    v91 = tree.num_children(tree._root.right)
    print(v91)

    tree = LinkedBST()
    lyst = [0, -1, -2, -3, 1, 2, 3]
    for i in lyst:
        tree.add(i)
    print(str(tree))
    print("balanced?", tree.isBalanced())
    tree.rebalance()
    print(str(tree))
    print(tree.isBalanced())


