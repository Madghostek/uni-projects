class Node:
    def __init__(self, x: int, y: int, parent_node=None) -> None:
        self._x = x
        self._y = y
        self._parent = parent_node
        # self._children = [] not needed

    def get_pos(self):
        return (self._x, self._y)

    def get_parent(self):
        return self._parent
