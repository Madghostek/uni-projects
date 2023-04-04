from bst import BinarySearchTree, Node


class AVLTree(BinarySearchTree):
    def __init__(self, initial_values) -> None:
        super().__init__(initial_values)

    def add(self, value, current_node=None):
        """
        Adds an element to the tree and updates balance afterwards
        """
        current_node = super().add(value)
        # updating balance of the parent node after adding element
        self._update_balance(current_node.getParent())

    def remove(self, value):
        changed_nodes = super().remove(value)
        for node in changed_nodes:
            if node:
                self._update_balance(node, removing=True)

    def _rotate_left(self, node):
        """
        A single rotation to the left
                (new_root)        (node)
               /     \            /
          (node)      c   <----  a    (new_root)
         /     \                        /    \
       a         b                     b      c
        """
        new_root = node.getRight()
        if not new_root:
            return
        node.setRight(new_root.getLeft())
        if new_root.getLeft() is not None:
            new_root.getLeft().setParent(node)
        new_root.setParent(node.getParent())
        # node is the root of the tree
        if node.getParent() is None:
            self.setRoot(new_root)
        else:
            if node.getParent() and node.getParent().getLeft() == node:
                node.getParent().setLeft(new_root)
            else:
                node.getParent().setRight(new_root)
        # change references between old(node) and new root
        new_root.setLeft(node)
        node.setParent(new_root)
        # change balance
        node.setBalance(node.getBalance() + 1 - min(new_root.getBalance(), 0))
        new_root.setBalance(new_root.getBalance() + 1 +
                            max(node.getBalance(), 0))

    def _rotate_right(self, node):
        """
        A single rotation to the right

                (node)           (new_root)
               /     \            /    \
       (new_root)     c  ---->  a       (node)
         /     \                        /    \
       a         b                     b      c

        """
        new_root = node.getLeft()
        if not new_root:
            return
        node.setLeft(new_root.getRight())
        new_root.setParent(node.getParent())
        # node is the root of the tree
        if node.getParent() is None:
            self.setRoot(new_root)
        else:
            if node.getParent() and node.getParent().getRight() == node:
                node.getParent().setRight(new_root)
            else:
                node.getParent().setLeft(new_root)
        # change references between old(node) and new root
        new_root.setRight(node)
        node.setParent(new_root)
        # change balance
        node.setBalance(node.getBalance() - 1 - max(new_root.getBalance(), 0))
        new_root.setBalance(new_root.getBalance() - 1 +
                            min(node.getBalance(), 0))

    # given a node, calculate it's balance
    def _update_balance(self, node, removing=False):
        rebalance_parent_later = False
        if not node:
            return
        new_bal = 0
        l, r = node.getLeft(), node.getRight()
        if l:
            new_bal = l.getHeight()
        if r:
            new_bal -= r.getHeight()
        old_bal = node.getBalance()
        if old_bal != new_bal:
            if (old_bal == 0 and new_bal != 0 and not removing) or (
                    old_bal != 0 and new_bal == 0 and removing):
                rebalance_parent_later = True
            node.setBalance(new_bal)
            if abs(new_bal) > 1:
                # here we must force rebalance, because we changed shape
                rebalance_parent_later = True
                self._rebalance(node)
                new_bal = 0
                if l:
                    new_bal = l.getHeight()
                if r:
                    new_bal -= r.getHeight()
                node.setBalance(new_bal)
            # this can happen when adding first child, or removing last child,
            # or rebalancing
            if rebalance_parent_later:
                self._update_balance(node.getParent())

    def _rebalance(self, node):
        if node.getBalance() < 0:
            # right case
            if node.getRight() and node.getRight().getBalance() > 0:
                # right left case
                self._rotate_right(node.getRight())
            # right right case
            self._rotate_left(node)
        elif node.getBalance() > 0:
            # left case
            if node.getLeft() and node.getLeft().getBalance() < 0:
                # left right case
                self._rotate_left(node.getLeft())
            # left left case
            self._rotate_right(node)


def main():
    data = [1, 7, 5, 4, 6, 3, 2, 9, 0]
    tree = AVLTree(data)
    bst_tree = BinarySearchTree(data)
    tree.printTree(tree.getRoot())
    tree.add(-4)
    print("\n-----------------------------\n")
    tree.printTree(tree.getRoot())
    tree.remove(1)
    tree.remove(6)
    tree.remove(9)
    # print("\n-----------------------------\n")
    # tree.printTree(tree.getRoot())
    # tree.remove(3)
    print("\n-----------------------------\n")
    tree.printTree(tree.getRoot())


if __name__ == "__main__":
    main()
