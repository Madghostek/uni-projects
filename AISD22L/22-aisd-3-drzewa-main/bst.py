class Node:
    def __init__(self, value, left=None, right=None, parent=None, balance=0) -> None:
        self._value = value
        self._left = left
        self._right = right
        self._parent = parent
        self._balance = balance

    def getValue(self):
        return self._value

    def setValue(self, new_value):
        self._value = new_value

    def getParent(self):
        return self._parent

    def setParent(self, new_parent):
        self._parent = new_parent

    def getLeft(self):
        return self._left

    def getRight(self):
        return self._right

    def setLeft(self, new_node):
        self._left = new_node
        if new_node:
            new_node.setParent(self)

    def setRight(self, new_node):
        self._right = new_node
        if new_node:
            new_node.setParent(self)

    def getBalance(self):
        return self._balance

    def setBalance(self, new_balance):
        self._balance = new_balance

    def getHeight(self, offset=0):
        r, l = self.getRight(), self.getLeft()
        rh = r.getHeight() if r else 0
        lh = l.getHeight() if l else 0
        return 1+max(rh, lh)


class BinarySearchTree:
    def __init__(self, initial_values=None) -> None:
        self._root = None
        if initial_values is not None:
            for value in initial_values:
                self.add(value)

    def getRoot(self):
        return self._root

    def setRoot(self, new_root):
        self._root = new_root

    def add(self, val):
        if not self._root:
            self._root = Node(val)
            return self._root
        current_node = self._root
        while current_node is not None:
            if current_node.getValue() < val:
                right = current_node.getRight()
                if not right:
                    current_node.setRight(Node(val, parent=current_node))
                    current_node = current_node.getRight()
                    break
                else:
                    current_node = right
            else:
                left = current_node.getLeft()
                if not left:
                    current_node.setLeft(Node(val, parent=current_node))
                    current_node = current_node.getLeft()
                    break
                else:
                    current_node = left

        return current_node

    def find(self, val):
        if not self._root:
            return
        current_node = self._root
        while current_node is not None:
            if current_node.getValue() < val:
                right = current_node.getRight()
                if not right:
                    return None
                else:
                    current_node = right
            elif current_node.getValue() > val:
                left = current_node.getLeft()
                if not left:
                    return None
                else:
                    current_node = left
            else:
                return current_node

    # return next closest (by value) node to base node being removed
    # generally:
    #    1. get right tree
    #    2. traverse left trees as far as possible, succesor is the last possible one
    #       2a. if right subtree has not left subtrees, return right node
    def _remove_find_successor(self, base):
        right = base.getRight()  # 1
        # if not right: # this will never happen during deleting
        left = right.getLeft()  # 2
        prev = left
        while left is not None:
            prev = left
            left = left.getLeft()
        if prev:  # 2a
            return prev
        return right

    # returns list of nodes for AVL which will need recalculating
    def remove(self, value):
        to_remove = self.find(value)
        # special case, element to remove is a leaf (or has no right subtree)
        if to_remove.getRight() is None:
            cur_parent = to_remove.getParent()
            # are we removing root?
            if not cur_parent:
                self._root = to_remove.getLeft()
            elif cur_parent.getRight() == to_remove:  # is it a right-hanging leaf?
                cur_parent.setRight(to_remove.getLeft())
            else:
                cur_parent.setLeft(to_remove.getLeft())
            return [cur_parent]

        # general case, find the successor
        # we know to_remove MUST have right subtree
        s = self._remove_find_successor(to_remove)
        parent = to_remove.getParent()

        # if we are removing root, set root value to successor
        if not parent:
            self._root.setValue(s.getValue())
        # removing normal node
        else:
            # write successor value in place of the thing being removed
            to_remove.setValue(s.getValue())
        # remove the successor at bottom, there are two cases, however we must complete the link which we are destoying
        # so we cant just do s.getParent().setLeft(None)
        right_subtree_of_successor = s.getRight()
        s_parent_ref = s.getParent()  # remember before s gets nuked

        # before overwriting again find out if successor was right or left
        if s.getParent().getLeft() is s:
            s.getParent().setLeft(
                right_subtree_of_successor
            )  # it may be None, we don't care
        else:
            s.getParent().setRight(
                right_subtree_of_successor
            )  # it may be None, we don't care

        return [s.getParent(), to_remove]

    def printTree(self, node, level=0):
        if node is not None:
            self.printTree(node.getRight(), level + 1)
            print(" " * 4 * level + "**" + str(node.getValue()))
            self.printTree(node.getLeft(), level + 1)


def main():
    data = [1, 7, 5, 4, 6, 3, 2, 9, 0]
    tree = BinarySearchTree(data)
    a = tree.find(4)
    tree.printTree()
    tree.remove(1)
    tree.printTree()
    tree.printTree(tree.getRoot())
    pass


if __name__ == "__main__":
    main()
