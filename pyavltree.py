import random
import math


class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0

    def __str__(self):
        return "Key: " + str(self.data) + " Height: " + str(self.height)

    def is_leaf(self):
        """ Return True if Leaf, False Otherwise
        """
        return self.height == 0

    def max_child_height(self):
        """ Return Max Child Height or -1 if No Children
        """
        if self.left_child and self.right_child:
            return max(self.left_child.height, self.right_child.height)
        elif self.left_child and not self.right_child:
            return self.left_child.height
        elif not self.left_child and self.right_child:
            return self.right_child.height
        else:
            return -1

    def weigh(self):
        """ Return How Left or Right Sided the Tree Is
        Positive Number Means Left Side Heavy, Negative Number Means Right Side Heavy
        """
        return (self.left_child.height if self.left_child else -1) - (self.right_child.height if self.right_child else -1)

    def rotate_right(self):
        # assign variables
        to_demote = self
        top = to_demote.parent
        to_promote = to_demote.right_child
        swapper = to_promote.left_child

        # swap children
        to_promote.left_child = to_demote
        to_demote.right_child = swapper

        # re-assign parents
        to_promote.parent = top
        to_demote.parent = to_promote
        swapper.parent = to_demote

        if top is None:
            top = to_promote
        elif top.right_child == to_demote:
            top.right_child = to_promote
        else:
            top.left_child = to_promote

        return top

    def rotate_left(self):
        # assign variables
        to_demote = self
        top = to_demote.parent
        to_promote = to_demote.left_child
        swapper = to_promote.right_child

        # swap children
        to_promote.right_child = to_demote
        to_demote.left_child = swapper

        # re-assign parents
        to_promote.parent = top
        to_demote.parent = to_promote
        swapper.parent = to_demote

        if top is None:
            top = to_promote
        elif top.right_child == to_demote:
            top.right_child = to_promote
        else:
            top.left_child = to_promote

        return top


def update_node_height(node):
    changed = True
    while node and changed:
        old_height = node.height
        node.height = (node.max_child_height() + 1 if (node.right_child or node.left_child) else 0)
        changed = node.height != old_height
        node = node.parent


class AVLTree():
    def __init__(self, *args):
        self.root = None  # root Node
        self.element_count = 0
        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def __len__(self):
        return self.element_count

    def height(self):
        """ Return Max Height Of Tree
        """
        if self.root:
            return self.root.height
        else:
            return 0

    def balance(self, node):
        """ Perform balancing Operation
        """
        top = node.parent  # allowed to be NULL
        while node.weigh() < -1 or node.weigh() > 1:
            if node.weigh() == -2:
                # right side heavy

                if node.right_child.weigh() < 0:
                    # right-side left-side heavy
                    node.right_child = node.right_child.rotate_left()
                    self.recompute_heights(node.right_child)

                # right-side right-side heavy
                new_top = node.rotate_right()
                if new_top.parent is None:
                    self.root_node = node
                self.recompute_heights(new_top)
            else:
                # left side heavy

                if node.left_child.weigh() > 0:
                    # left-side right-side heavy
                    node.left_child = node.left_child.rotate_right()
                    self.recompute_heights(node.left_child)

                # left-side left-side heavy
                new_top = node.rotate_left()
                if new_top.parent is None:
                    self.root_node = node
                self.recompute_heights(new_top)


    def rotate_right(self):
        pass

    def rotate_left(self):
        pass

    def sanity_check(self, *args):
        if len(args) == 0:
            node = self.root
        else:
            node = args[0]
        if (node is None) or (node.is_leaf() and node.parent is None):
            # trivial - no sanity check needed, as either the tree is empty or there is only one node in the tree
            pass
        else:
            if node.height != node.max_children_height() + 1:
                raise Exception("Invalid height for node " + str(node) + ": " + str(node.height) + " instead of " + str(node.max_children_height() + 1) + "!")

            bal_factor = node.balance()
            #Test the balance factor
            if not (-1 <= bal_factor <= 1):
                raise Exception("Balance factor for node " + str(node) + " is " + str(bal_factor) + "!")
                #Make sure we have no circular references
            if not (node.left_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.left_child is node!")
            if not (node.right_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.right_child is node!")

            if node.left_child:
                if not (node.left_child.parent == node):
                    raise Exception("Left child of node " + str(node) + " doesn't know who his father is!")
                if not (node.left_child.key <= node.key):
                    raise Exception("Key of left child of node " + str(node) + " is greater than key of his parent!")
                self.sanity_check(node.left_child)

            if node.right_child:
                if not (node.right_child.parent == node):
                    raise Exception("Right child of node " + str(node) + " doesn't know who his father is!")
                if not (node.right_child.key >= node.key):
                    raise Exception("Key of right child of node " + str(node) + " is less than key of his parent!")
                self.sanity_check(node.right_child)


    def add_as_child(self, parent_node, child_node):
        node_to_rebalance = None
        if child_node.key < parent_node.key:
            if not parent_node.left_child:
                parent_node.left_child = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_child_height() + 1
                        if not node.weigh() in [-1, 0, 1]:
                            node_to_rebalance = node
                            break  # we need the one that is furthest from the root
                        node = node.parent
            else:
                self.add_as_child(parent_node.left_child, child_node)
        else:
            if not parent_node.right_child:
                parent_node.right_child = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_child_height() + 1
                        if not node.weigh() in [-1, 0, 1]:
                            node_to_rebalance = node
                            break  # we need the one that is furthest from the root
                        node = node.parent
            else:
                self.add_as_child(parent_node.right_child, child_node)

        if node_to_rebalance:
            self.balance(node_to_rebalance)

    def insert(self, key):
        new_node = Node(key)
        if not self.root:
            self.root = new_node
        else:
            if not self.find(key):
                self.element_count += 1
                self.add_as_child(self.root, new_node)

    @staticmethod
    def find_biggest(start_node):
        node = start_node
        while node.right_child:
            node = node.right_child
        return node

    @staticmethod
    def find_smallest(start_node):
        node = start_node
        while node.left_child:
            node = node.left_child
        return node

    def inorder_non_recursive(self):
        node = self.root
        retlst = []
        while node.left_child:
            node = node.left_child
        while node:
            retlst += [node.key]
            if node.right_child:
                node = node.right_child
                while node.left_child:
                    node = node.left_child
            else:
                while node.parent and (node == node.parent.right_child):
                    node = node.parent
                node = node.parent
        return retlst

    def preorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        retlst += [node.key]
        if node.left_child:
            retlst = self.preorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.preorder(node.right_child, retlst)
        return retlst

    def inorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.inorder(node.left_child, retlst)
        retlst += [node.key]
        if node.right_child:
            retlst = self.inorder(node.right_child, retlst)
        return retlst

    def postorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.postorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.postorder(node.right_child, retlst)
        retlst += [node.key]
        return retlst

    def as_list(self, pre_in_post):
        if not self.root:
            return []
        if pre_in_post == 0:
            return self.preorder(self.root)
        elif pre_in_post == 1:
            return self.inorder(self.root)
        elif pre_in_post == 2:
            return self.postorder(self.root)
        elif pre_in_post == 3:
            return self.inorder_non_recursive()

    def find(self, key):
        return self.find_in_subtree(self.root, key)

    def find_in_subtree(self, node, key):
        if node is None:
            return None  # key not found
        if key < node.key:
            return self.find_in_subtree(node.left_child, key)
        elif key > node.key:
            return self.find_in_subtree(node.right_child, key)
        else:  # key is equal to node key
            return node

    def remove(self, key):
        # first find
        node = self.find(key)

        if not node is None:
            self.element_count -= 1

            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.

            if node.is_leaf():
                self.remove_leaf(node)
            elif (bool(node.left_child)) ^ (bool(node.right_child)):
                self.remove_branch(node)
            else:
                assert node.left_child and node.right_child
                self.swap_with_successor_and_remove(node)

    def remove_leaf(self, node):
        parent = node.parent
        if parent:
            if parent.left_child == node:
                parent.left_child = None
            else:
                assert (parent.right_child == node)
                parent.right_child = None
            self.recompute_heights(parent)
        else:
            self.root = None
        del node
        # rebalance
        node = parent
        while node:
            if not node.weigh() in [-1, 0, 1]:
                self.balance(node)
            node = node.parent

    def remove_branch(self, node):
        parent = node.parent
        if parent:
            if parent.left_child == node:
                parent.left_child = node.right_child or node.left_child
            else:
                assert (parent.right_child == node)
                parent.right_child = node.right_child or node.left_child
            if node.left_child:
                node.left_child.parent = parent
            else:
                assert node.right_child
                node.right_child.parent = parent
            self.recompute_heights(parent)
        del node
        # rebalance
        node = parent
        while node:
            if not node.weigh() in [-1, 0, 1]:
                self.balance(node)
            node = node.parent

    def swap_with_successor_and_remove(self, node):
        successor = self.find_smallest(node.right_child)
        self.swap_nodes(node, successor)
        assert (node.left_child is None)
        if node.height == 0:
            self.remove_leaf(node)
        else:
            self.remove_branch(node)

    def swap_nodes(self, node_1, node_2):
        assert (node_1.height > node_2.height)
        parent_1 = node_1.parent
        left_child_1 = node_1.left_child
        right_child_1 = node_1.right_child
        parent_2 = node_2.parent
        assert (not parent_2 is None)
        assert (parent_2.left_child == node_2 or parent_2 == node_1)
        left_child_2 = node_2.left_child
        assert (left_child_2 is None)
        right_child_2 = node_2.right_child

        # swap heights
        tmp = node_1.height
        node_1.height = node_2.height
        node_2.height = tmp

        if parent_1:
            if parent_1.left_child == node_1:
                parent_1.left_child = node_2
            else:
                assert (parent_1.right_child == node_1)
                parent_1.right_child = node_2
            node_2.parent = parent_1
        else:
            self.root = node_2
            node_2.parent = None

        node_2.left_child = left_child_1
        left_child_1.parent = node_2
        node_1.left_child = left_child_2  # None
        node_1.right_child = right_child_2
        if right_child_2:
            right_child_2.parent = node_1
        if not (parent_2 == node_1):
            node_2.right_child = right_child_1
            right_child_1.parent = node_2

            parent_2.left_child = node_1
            node_1.parent = parent_2
        else:
            node_2.right_child = node_1
            node_1.parent = node_2

            # use for debug only and only with small trees

    def out(self, start_node=None):
        if start_node is None:
            start_node = self.root
        space_symbol = "*"
        spaces_count = 80
        out_string = ""
        initial_spaces_string = space_symbol * spaces_count + "\n"
        if not start_node:
            return "AVLTree is empty"
        else:
            level = [start_node]
            while len([i for i in level if (not i is None)]) > 0:
                level_string = initial_spaces_string
                for i in xrange(len(level)):
                    j = (i + 1) * spaces_count / (len(level) + 1)
                    level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j + 1:]
                level_next = []
                for i in level:
                    level_next += ([i.left_child, i.right_child] if i else [None, None])
                level = level_next
                out_string += level_string
        return out_string


def random_data_generator(max_r):
    for i in xrange(max_r):
        yield random.randint(0, max_r)


def test():
    """check empty tree creation"""
    a = AVLTree()
    a.sanity_check()

    """check not empty tree creation"""
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    seq_copy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    #random.shuffle(seq)
    b = AVLTree(seq)
    b.sanity_check()

    """check that inorder traversal on an AVL tree 
    (and on a binary search tree in the whole) 
    will return values from the underlying set in order"""
    assert (b.as_list(3) == b.as_list(1) == seq_copy)

    """check that node deletion works"""
    c = AVLTree(random_data_generator(10000))
    before_deletion = c.element_count
    for i in random_data_generator(1000):
        c.remove(i)
    after_deletion = c.element_count
    c.sanity_check()
    assert (before_deletion >= after_deletion)
    #print c.out()

    """check that an AVL tree's height is strictly less than 
    1.44*log2(N+2)-1 (there N is number of elements)"""
    assert (c.height() < 1.44 * math.log(after_deletion + 2, 2) - 1)
