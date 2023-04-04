from typing import List, Tuple
from numpy.typing import NDArray

from mapsolver.mynode import Node


class MapSolver():
    '''
    Class that is used to talk with map solver alghoritm.
    Some functions could be private,
    but they could be useful for a programmer outside of the solving process

    The class goes into solved state after calling solve_map(),
    after that the solution is accesible with getSolution().
    '''

    def __init__(self) -> None:
        self._solution = None
        self._array = None

    def getSolution(self) -> List:
        if self._solution is None:
            raise Exception("Call solve_map")
        return self._solution

    def is_pos_valid(self, pos: Tuple[int]) -> bool:
        '''
        Takes an (x,y) tuple and checks if its a valid point on map
        '''
        # bound is 1 bigger than maximum index, hence the 0 <= ... < bound
        bound = self._array.shape[0]
        if 0 <= pos[0] < bound and 0 <= pos[1] < bound:
            return True
        return False

    def get_height_at(self, pos: Node) -> float:
        '''
        returns value on map for given Node pos
        '''
        return self._array[pos]

    def solve_graph(self, input: NDArray, min_depth: float, start: Node) -> bool:
        '''
        Finds path to n-1,n-1 using BFS, then fills solution array.
        After function finishes, either returns True or False.
        Visited places are marked with values>min_depth,
        so they don't get considered
        '''

        # 1.Check if current tile is end (n-1,n-1), finish search if yes
        # 2.Spread nodes to all 3 directions, or less if blocked
        # 3.Return True if any node returned true

        # dont modify the actual array because it might be used by frontend
        self._array = input.copy()

        # special case, ocean has 1 tile (numpy doesnt like this)
        if input.size == 1:
            if input[0] <= min_depth:
                self._solution = [(0, 0)]
                return True
            else:
                return False
        # initial checks, is starting point in-bounds?
        if not self.is_pos_valid(start.get_pos()):
            return False
        # Can the ship even be here?
        if input[start.get_pos()] > min_depth:
            return False

        queue = [start]
        # this is how visited places are marked
        self._array[start.get_pos()] = min_depth+1
        ocean_size = input.shape[0]
        while len(queue):
            new_queue = []
            for node in queue:
                cur_pos = node.get_pos()
                if cur_pos == (ocean_size-1, ocean_size-1):
                    # We are at the end, get list of steps
                    steps = []
                    while node is not None:
                        steps.insert(0, node.get_pos())
                        node = node.get_parent()
                    self._solution = steps
                    return True
                # we are not at end, deploy more nodes,
                # order down right up left
                nextlist = [(cur_pos[0], cur_pos[1]+1),
                            (cur_pos[0]+1, cur_pos[1]),
                            (cur_pos[0], cur_pos[1]-1),
                            (cur_pos[0]-1, cur_pos[1])]

                for next in nextlist:
                    # splitting because line too long
                    if self.is_pos_valid(next):
                        if self.get_height_at(next) <= min_depth:
                            new_queue.append(Node(*next, node))
                            self._array[next] = min_depth+1

            # replace previous queue with new active nodes
            queue = new_queue
        # There is no solution
        self._solution = []
        return False

    def solve_map(self, input: NDArray, min_depth: float) -> List[tuple]:
        """
        Finds best solution for given input ocean map and minimum allowed depth
        Solution can be accessed with get_solution()
        If map is unsolvable returns False, otherwise True
        :param input: numpy matrix (or 2d list) describing the ocean floor
        :param max_depth: how deep the water must be
        :return: True if solvable
        """
        if input.size == 0:
            raise Exception("Ocean can't be empty")
        return self.solve_graph(input, min_depth, Node(0, 0))
