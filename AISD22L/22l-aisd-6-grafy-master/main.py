import heapq # (value_for_comparison, additional_data)
import sys

def find_zero(tab):
    list_of_zeros = []
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if tab[i][j] == '0':
                list_of_zeros.append((j,i))
    return list_of_zeros

# returns list of (x,y) that are valid unvisited neighbors
def get_neighbors_for_xy(point, board, visited):
    all_neighbors = [(point[0]+1, point[1]), (point[0]-1, point[1]), (point[0], point[1]+1), (point[0], point[1]-1)]
            # remove invalid or visited
    i = 0
    while (i < 4):
        value = all_neighbors[i]
        return [value for value in all_neighbors if value not in visited and value[0] >= 0 and value[0] < len(board[0]) and value[1] >= 0 and value[1] < len(board)]

def main():
    filename = sys.argv[1]
    print(filename)
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.rstrip())
    zeros = find_zero(lines)
    if len(zeros)!=2:
        return -1
    root,end = zeros[0],zeros[1]
    #print("start,end",root,end)
    #print("xlen,ylen:",len(lines[0]),len(lines))
    # (int value, tuple xy)
    queue = [(0,root)] # heap
    distances = {root : 0}
    visited = []
    prev = {} # this can be a dict as well
    current = None
    while len(queue):
        current = heapq.heappop(queue) # heap ensures this will be the smallest element
        #print("\ncurrent:",current)
        if (current[1]==end):
            break
        visited.append(current[1]) # mark as visited
        # get list of neighbors
        all_neighbors=get_neighbors_for_xy(current[1], lines, visited)

        # update path lengths for all neighbors - if distance[current]+value[v] is better than distance[v], update
        # or if the distance is not known yet
        for v in all_neighbors:
            #print("check:", v)
            value = (int(lines[v[1]][v[0]]))
            
            if v not in distances:
                # it didn't exist yet
                distances[v]=distances[current[1]]+value
                prev[v]=current[1]
                #print("push:",(distances[v],v))
                heapq.heappush(queue, (distances[v],v))
            elif distances[v]>distances[current[1]]+value:
                # it is aleady waiting for processing, but wasn't choosen due to high cost,
                # update but don't add again to heap
                distances[v]=distances[current[1]]+value
                prev[v]=current[1]

    # everything is processed, print path...
    # current should hold the '0' end point
    solution = [end]
    current = end
    while (current!=root):
        print(current)
        current = prev[current]
        solution.append(current)

    # make viual solution
    print("*"*(len(lines[0])+2))
    print("*", end="")
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if (x,y) in solution:
                print(lines[y][x], end="")
            else:
                print(" ", end="")
        print("*\n*", end="") # newline
    print("*"*(len(lines[0])+1))

    
        


if __name__ == "__main__":
    main()
