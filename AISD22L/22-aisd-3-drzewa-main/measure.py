from bst import BinarySearchTree, Node
from avl import AVLTree
import time
import random
import gc
from matplotlib import pyplot as plt

gTree = None


def measure_function(fun, in_array, iter=1):
    """
    helper function to measure execution, disables gc
    :param fun: function reference
    :param in_array: data passed to function
    :param iter: amount of iterations
    :return: average time taken (in milliseconds), max deviation
    """

    gc_old = gc.isenabled()  # pobierz aktualny stan odśmiecania gc.disable()
    gc.disable()
    # measure
    results = []
    for i in range(iter):
        start = time.time()
        fun(in_array)
        delta = time.time()-start
        results.append(delta)

    if gc_old:
        gc.enable()
    avg = sum(results)/len(results)
    biggest_deviation = max(abs(avg-max(results)), abs(avg-min(results)))
    return avg, biggest_deviation

# there is microscopic overhead from loop


def tree_finder(everything_to_find):
    global gTree
    for x in everything_to_find:
        gTree.find(x)


def tree_deleter(everything_to_delete):
    global gTree
    for x in everything_to_delete:
        if x == 21:
            pass
        print("")
        print("-------")
        print("removing", x)
        gTree.printTree(gTree._root)
        gTree.remove(x)


def treecopy(original: Node):
    """
    Clones a BST recursively
    :param original: object to copy
    :return: new copied tree
    """
    if original is None:
        return None
    new = Node(original.getValue())
    new.setLeft(treecopy(original.getLeft()))
    new.setRight(treecopy(original.getRight()))
    return new


def draw_functions_on_one_plot(data):
    # draw all functions on one plot
    for name, times in data.items():
        x = [time[0] for time in times]
        y = [time[1] for time in times]
        plt.plot(x, y, label=name)
        plt.xlabel('Tree size')
        plt.ylabel('Time(s)')
    plt.legend()
    plt.title('All algorithms')
    plt.savefig('all.jpg', format='jpg', dpi=200)


def draw_separately(data):
    # draw each function on separate plot
    for name, times in data.items():
        plt.figure()
        x = [time[0] for time in times]
        y = [time[1] for time in times]
        plt.plot(x, y)
        plt.xlabel('Tree size')
        plt.ylabel('Time(s)')
        plt.title(name)
        plt.savefig(name+'.jpg', format='jpg', dpi=200)


def main():
    global gTree
    x_amount = 50000
    cases = range(1000, x_amount+1, 1000)

    data = random.sample(range(x_amount), x_amount)
    # print(data)
    # data to plot
    results = {
        "bst_create": [],
        "bst_find": [],
        "bst_remove": [],
        "avl_create": [],
        "avl_find": [],
        "avl_remove": [],
    }

    for case in cases:
        print("[BST] creating", case)
        results['bst_create'].append([case, measure_function(BinarySearchTree, data[:case])[
                                     0]])  # passing class so construtor is measured

    gTree = BinarySearchTree(data)  # now create a tree for next tests

    # finding
    for case in cases:
        print("[BST] finding", case)
        results['bst_find'].append(
            [case, measure_function(tree_finder, data[:case])[0]])

    # deleting
    backup = BinarySearchTree([gTree._root.getValue()])
    backup._root = treecopy(gTree._root)
    for case in cases:
        print("[BST] deleting", case)

        results['bst_remove'].append(
            [case, measure_function(tree_deleter, data[:case])[0]])
        del gTree._root
        gTree._root = treecopy(backup._root)

    # AVL
    # creating
    for case in cases:
        print("[AVL] creating", case)
        results['avl_create'].append(
            [case, measure_function(AVLTree, data[:case])[0]])

    gTree = AVLTree(data)  # now create a tree for next tests

    # finding
    for case in cases:
        print("[AVL] finding", case)
        results['avl_find'].append(
            [case, measure_function(tree_finder, data[:case])[0]])

    # deleting
    backup = AVLTree([])
    backup._root = treecopy(gTree._root)
    for case in cases:
        print("[AVL] deleting", case)
        results['avl_remove'].append(
            [case, measure_function(tree_deleter, data[:case])[0]])
        del gTree._root
        gTree._root = treecopy(backup._root)

    draw_separately(results)
    draw_functions_on_one_plot(results)


main()

# crash = [1, 6, 4, 2, 9, 7, 0, 8, 3, 5]
# treec = AVLTree(crash)
# gTree = treec
# gTree.printTree(gTree._root)
# tree_deleter(crash)

# treecopy test
# a = BinarySearchTree([1,3,4,6,7,8,13,2,4,9])
# a.printTree(a._root)
# b = BinarySearchTree()
# b._root = treecopy(a._root)
# b.printTree(b._root)
