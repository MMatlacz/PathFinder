# coding=utf-8
import sys
from Queue import PriorityQueue


def calculate_path(filename="miasta.txt"):
    nodes = read_file(filename)
    nodes = create_graph(nodes)
    return nodes


class Node:
    adjacencies = []  # Edge[]
    minDistance = float("inf")
    previous = None

    def get_mindist(self):
        return self.minDistance

    def get_adjencies(self):
        return self.adjacencies

    def __init__(self, arg_name):
        self.name = arg_name

    def __str__(self):
        return self.name

    def __cmp__(self, other):
        return float(cmp(self.minDistance, other.minDistance))


class Edge:
    def __init__(self, arg_target, arg_weight):
        self.target = arg_target
        self.weight = arg_weight


def read_file(filename):
    content = []

    with open(filename) as f:
        lines = f.readlines()
        f.close()
    for line in lines:
        path = line.split(" ")
        content.append(path)
    return content


def create_graph(node_file):
    nodes = {}
    for line in node_file:
        nodes[line[0].strip()] = Node(line[0].strip())
        nodes[line[2].strip()] = Node(line[2].strip())
    for line in node_file:
        nodes.get(line[0]).adjacencies.append(
                Edge(
                        nodes.get(line[2].strip()),
                        float(line[1].strip())
                )
        )
        nodes.get(line[2].strip()).adjacencies.append(
                Edge(
                        nodes.get(line[0].strip()),
                        float(line[1].strip())
                )
        )
    return nodes


def compute_paths(source):
    source.minDistance = 0.
    node_queue = PriorityQueue()
    node_queue.put(source)

    while not node_queue.empty():

        u = node_queue.get()

        # Visit each edge exiting u
        for e in u.adjacencies:
            v = e.target
            weight = e.weight
            distance_through_u = u.minDistance + weight
            if distance_through_u < v.minDistance:
                #node_queue.get(v)

                v.minDistance = distance_through_u
                v.previous = u
                node_queue.put(v)


def get_shortest_path_to(target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = node.previous

    path.reverse()
    return path

start = sys.argv[1]
end = sys.argv[2]
nodes = calculate_path(filename="miasta-kopia.txt")
compute_paths(nodes.get(start))
path = get_shortest_path_to(nodes.get(end))
print("Distance to " + str(nodes.get(end)) + ": " + str(nodes.get(end).get_mindist()))
for p in path:
    print(p)
