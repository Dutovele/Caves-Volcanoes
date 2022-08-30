
from collections import defaultdict

num_vertices = 0
num_edges = 0
paths_num = 0
point_type_list = [0]*num_vertices
paths = []


class Stack:
  def __init__(self):
    self.container = []

  def is_empty(self):
    return len(self.container) == 0

  def push(self, node):
    self.container.append(node)

  def pop(self):
    return self.container.pop()


"""In order to store the information about the caves and volcanoes in the park we use graph data structure.
This way we can create a dictionary to store the edges between nodes - paths connecting caves and volcanoes.
For example: 1: [0, 2 ,4, 5] The node 1 has connections to 0, 2, 4, 5"""
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    # point_type: 0 - "cave", 1 - "volcano"
    def addEdge(self, u, v):
        self.graph[u].append(v)

    """ Inside the Graph we create a function to perform Depth First Search so that we can traverse the nodes in the graph"""
    def DFS(self):

        # We will need the mark the nodes that we visited, so we create an array with length of number of nodes
        visited = [False] * num_vertices
        # We create a stack to store the nodes while processing them
        stack = Stack()

        # We add the first node from our caves list (as
        stack.push(caves_list[0])
        # We mark the first node we process as visited
        visited[caves_list[0]] = True
        # We create a paths_num variable where we will add up the number of paths we find
        paths_num = 0

        # We create a loop to go through all the nodes that will appear in the stack.
        while (not stack.is_empty()):
            # we get a node from stack
            node = stack.pop()
            # print("PROCESSING NODE", node)
            # the nodes connected to it we save as nbrs
            nbrs = g.graph[node]

            conn_vol = [] # for each cave node we separate the volcanoes list connected to it
            if point_type_list[node] == 0:
                # if a node is connected to more than 1 other nodes
                if len(nbrs) > 1:
                    # print("The current cave", node, "its neighbours ", g.graph[node])
                    # we go through the neighbours of the node we are processing
                    for i in nbrs:
                        # check if the node is a cave type or volcano type
                        # volcano is marked as 1, so we append it to connected volcanoes list of that node
                        if point_type_list[i] == 1:
                            conn_vol.append(i)
                    # print("Node", node, "connected volcanoes", conn_vol)
                    # After we collected all volcano nodes connected to the cave-node we are processing
                    # we check if those volcano-nodes are connected to caves
                    for n in range(len(conn_vol)):
                        for m in range(1, len(conn_vol)):
                            # we filter so that we don´t need to process the lists twice, for ex. 1-4, not 4-1
                            if n < m:
                                # we check in the graph
                                # print("conn_vol", conn_vol)
                                for x in g.graph[conn_vol[n]]:
                                    for y in g.graph[conn_vol[m]]:
                                        # if two volcano-nodes that are connected to the original node are connected
                                        # to the same cave-node which differs from the original cave-node we parted from
                                        # then we add two paths to our path counting variable
                                        if x == y and point_type_list[x] == 0 and x != node:
                                            paths_num += 2
                                            # We can print the path we found
                                            p1 = [node, conn_vol[n], x, conn_vol[m], node]
                                            p2 = [node, conn_vol[m], x, conn_vol[n], node]
                                            print(p1)
                                            print(p2)
            # When we have counted all paths which leave from one cave node, we append the new cave node
            # while we mark the cave-node we have just processed as visited
            for n in nbrs:
                if not visited[n]:
                    stack.push(n)
                    visited[n] = True

        print("Num paths ", paths_num)

"""The function saves the input data from a text file and creates a graph in a form of a dictionary"""
def create_graph_from_file(dir):
    global num_vertices
    global num_edges
    global point_type_list

    line_number = 0

    file = open(dir, 'r')

    for line in file:
        if line_number == 0:
            num_vertices, num_edges = line.split()

            num_vertices = int(num_vertices)
            num_edges = int(num_edges)
            # print(num_vertices, num_edges)
            # Here we create a list of zeros in which we will update to "1" those vertices which are volcanoes
            # we will leave the vertices which are caves as "0"
            point_type_list = [0] * num_vertices
            # we save g.V as number of vertices in the graph
            g.V = num_vertices

        # we save the coonections between nodes into a dictionary
        elif line_number > 0 and line_number < num_edges+1:
            templine = line.strip("\n")
            v1, v2 = templine.split()
            v1 = int(v1)
            v2 = int(v2)
            # print(v1,v2)
            g.addEdge(v1,v2)
            g.addEdge(v2,v1)

        # we save the type of the node (volcano or cave) in a point_type_list
        # in which the nodes which are volcanoes are represented by 1 and caves, by 0.
        else:
            templine = line.strip("\n")
            v, point_type = templine.split()
            v = int(v)
            # print(v, point_type)
            if point_type == "V":
                point_type_list[v] = 1

        line_number += 1

    file.close()

"""This function gets from the list of node types a separate list - caves list (containing all nodes specified as caves)"""
def get_caves_list():
    global point_type_list

    caves_list = []

    for i in range(len(point_type_list)):
        if point_type_list[i] == 0:
            caves_list.append(i)

    return caves_list


# First we create a graph
g = Graph(num_vertices)
# We call our function which fills the graph with the data we have in the input
create_graph_from_file('inputdata/pub01.in')
# We create the list of nodes which are specified as caves as we need to start the path with a cave
caves_list = get_caves_list()
# We call Depth First Search  on the graph to find the paths and count their number
g.DFS()