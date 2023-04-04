class NHeap:
    def __init__(self, n: int, initial_values=None):
        self.n = n
        self._array = []
        # [root,
        # 	1, 2, 3, ..., n,
        # 	11, 12, 13, ..., 1n, 21, 22, 23, ..., 2n, ... nn]
        # each layer i has n^i nodes

        if initial_values:
            for x in initial_values:
                self.add(x)

    def getFirstChildIndex(self, parent_idx):
        return parent_idx * self.n + 1

    def printHeap(self, index=0, indent=0, count="R"):
        """
        Prints the heap, "child_n:value", each level has bigger indent, R is root
        """
        print("\t" * indent, end="")
        print(f"{count}:{self._array[index]}")
        child_idx = self.getFirstChildIndex(index)
        nr_of_child = 1
        for c in range(child_idx, child_idx + self.n):
            if c > len(self._array) - 1:
                break
            self.printHeap(c, indent + 1, nr_of_child)  # recursively print all children
            nr_of_child += 1

    def pop(self):
        """
        Remove root, also return that value, assumes heap was correct before removing
            1. remove root
            2. insert last element in _array to root
            3. find smallest/largest value from set (parent, children),
            first child index is parent_idx*n+1
            4. if smallest/largest is parent, end
            5. swap with smallest, goto 3
        """
        if not len(self._array):
            return None  # nothing to remove
        temp = self._array[0]
        popped = self._array.pop()
        if not len(self._array):
            return popped  # there was only the root, nothing more to do

        # replace root with the last node
        self._array[0] = popped

        parent_idx = 0
        # parent_idx - current operating index being checked
        # children - slice of main array that has all the children values
        while True:
            first_child_idx = self.getFirstChildIndex(parent_idx)
            children = self._array[first_child_idx:first_child_idx + self.n]
            if not len(children):
                break  # there was only the root left
            max_child = max(children)
            if max_child < self._array[parent_idx]:
                break  # if parent is bigger than children

            # there is no easy way to get the index of max element
            idx = 0  # offset inside slice
            for idx, val in enumerate(children):
                if val is max_child:
                    break

            # base + offset = absolute index in whole array
            idx += first_child_idx
            self._array[idx], self._array[parent_idx] = (
                self._array[parent_idx],
                self._array[idx],
            )
            # now the children that got swapped might need updating, but any other children is guaranteed to be heapified
            parent_idx = idx

        return temp

    def add(self, element: int):
        """
        Adds element and maitains the heap structure (swaps with higher
        elements), assumes the heap was correct before adding.
            1. append
            2. find parent index - (i-1)//n
            3. check if swap is needed, end if not
            4. swap, goto 2
        """
        self._array.append(element)
        new_idx = len(self._array) - 1

        while True:
            if not new_idx:  # this is root, break
                break
            parent = (new_idx - 1) // self.n

            # max heap
            if not self._array[parent] < self._array[new_idx]:
                break  # there is nothing to swap, break from loop (higher up in the heap it was correct before adding)
            self._array[parent], self._array[new_idx] = (
                self._array[new_idx],
                self._array[parent],
            )
            new_idx = parent
