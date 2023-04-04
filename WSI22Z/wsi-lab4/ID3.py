from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import math
import numpy as np

iris = load_iris()

x = iris.data
y = iris.target

# x_train -> y_train, próbki z całego zbioru do nauki, x wyznacza y
# x_test -> y_test, pozostałe próbki do przetestowania
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.1, random_state=123)


def entropy_func(class_count, num_samples):
    '''
    ratio between occurences of class in whole set
    '''
    freq = class_count/num_samples
    return freq*math.log(freq)


# used to calculate InfGain -> make groups based on atribute,
# find their entropy, easy to use
class Group:
    def __init__(self, group_classes):
        # array of classes in current tree part [0,1,2,1,2,0,...]
        self.group_classes = group_classes
        self.entropy = self.group_entropy()

    def __len__(self):
        return self.group_classes.size

    def group_entropy(self):
        s = 0.0
        unique = set(self.group_classes)
        for cl in unique:
            howmany = np.count_nonzero(self.group_classes == cl)
            s += -entropy_func(howmany, len(self.group_classes))
        return s


class Node:
    def __init__(self, split_feature, split_val, depth=None, child_node_a=None, child_node_b=None, val=None):
        self.split_feature = split_feature  # feature used to split
        self.split_val = split_val
        self.depth = depth
        self.child_node_a = child_node_a
        self.child_node_b = child_node_b
        self.val = val

    def predict(self, data):
        node = self
        while node.val is None:
            f, v = node.split_feature, node.split_val
            data_value = data[f]
            if data_value < v:
                node = node.child_node_a
            else:
                node = node.child_node_b
        return node.val


class DecisionTreeClassifier:
    def __init__(self, max_depth):
        self.depth = 0
        self.max_depth = max_depth
        self.tree = None

    @staticmethod
    # group_a is the subset of group_b
    def get_split_entropy(group_a, group_b):
        return (len(group_a)/len(group_b))*group_a.entropy

    def get_information_gain(self, parent_group, child_group_a, child_group_b):
        parentGroup = Group(parent_group)
        splitent = sum(self.get_split_entropy(Group(child), parentGroup)
                       for child in [child_group_a, child_group_b])
        return parentGroup.entropy-splitent

    def get_best_split(self, data, classes, which_feature_to_use):
        # go over all possible values...
        # first step is to get them
        possible_values = set(x[which_feature_to_use] for x in data)
        best_split = None
        best_gain = 0
        for point in possible_values:
            # get corresponding classes here instead of values
            a = [classes[idx] for idx, row in enumerate(
                data) if row[which_feature_to_use] >= point]
            first = np.asarray(a)

            second = np.asarray([classes[idx] for idx, row in enumerate(
                data) if row[which_feature_to_use] < point])
            gain = self.get_information_gain(classes, first, second)
            if gain > best_gain:
                best_gain = gain
                best_split = point
        return best_split, best_gain

    def get_best_feature_split(self, feature_values, classes):
        best_feature = 0
        best_split = 0
        best_gain = 0
        for feature in range(len(feature_values[0])):
            split, gain = self.get_best_split(feature_values, classes, feature)
            if gain > best_gain:
                best_gain = gain
                best_split = split
                best_feature = feature
        return best_feature, best_split

    def split_data_and_classes(self, data, classes, feature, value):
        '''
        returns two new children subsets divided by feature at value,
        feature is feature index (column number in dataset)
        '''
        classes_GE = [classes[idx] for idx, row in enumerate(
            data) if row[feature] >= value]
        classes_L = [classes[idx] for idx, row in enumerate(
            data) if row[feature] < value]
        data_GE = [data[idx] for idx, row in enumerate(
            data) if row[feature] >= value]
        data_L = [data[idx] for idx, row in enumerate(
            data) if row[feature] < value]
        return (data_L, classes_L), (data_GE, classes_GE)

    def build_tree(self, data, classes, depth=0):
        self.tree = self._build_tree_rec(data, classes, depth)

    def _build_tree_rec(self, data, classes, depth):
        ''' data - attributes
            classes - target class

            here use Node
        '''
        # albo depth wyczerpany, albo pozostała jedna klasa
        if depth == self.max_depth or len(set(classes)) == 1:
            # nie możemy dalej dzielić, patrzymy która klasa w tym momencie
            # jest najliczniejsza, ona będzie najprawdopodobniejsza
            # (lub jest jedyna)
            bestClass = np.argmax(np.bincount(classes))
            return Node(None, None, 0, None, None, bestClass)

        else:
            # patrzymy w jaki sposób najbardziej opłaca się podzielić
            best_feature, best_split = self.get_best_feature_split(
                data, classes)

            #  2 tuples (data, classes)
            partA, partB = self.split_data_and_classes(
                data, classes, best_feature, best_split)

            childA = self._build_tree_rec(np.asarray(
                partA[0]), np.asarray(partA[1]), depth+1)
            childB = self._build_tree_rec(np.asarray(
                partB[0]), np.asarray(partB[1]), depth+1)

            return Node(best_feature, best_split,
                        depth, childA, childB, None)

    def predict(self, data):
        return self.tree.predict(data)


# driver code
good_counter = 0

dc = DecisionTreeClassifier(3)
dc.build_tree(x_train, y_train)
for sample, gt in zip(x_test, y_test):
    prediction = dc.predict(sample)
    print(f"prediction/real:{prediction}/{gt}")
    if prediction == gt:
        good_counter += 1
percent = good_counter/len(y_test)*100
print(f"\nAccuracy: {good_counter}\{len(y_test)} ({percent:.2f}%)")
