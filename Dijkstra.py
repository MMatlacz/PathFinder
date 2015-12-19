# coding=utf-8
# metoda oblicza najkrótszą trasę między dwoma wybranymi miastami
import json
from Queue import PriorityQueue

import falcon

from Statics import getTemplate

template = getTemplate('index.html')


class Dijkstra(object):
    def __init__(self):
        pass

    def on_get(self, req, resp, start, end):
        compute_paths(start)
        resp.body = json.dumps(get_shortest_path_to(end))
        # resp.body = template.render(data="LOL it's working")
        resp.content_type = 'text/html'
        resp.status = falcon.HTTP_200

    def calculate_path(self, filename="miasta.txt"):
        nodes = read_file(filename)
        nodes = create_graph(nodes)
        return nodes


class Node:
    adjacencies = []  # Edge[]
    minDistance = float("inf")
    previous = None

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
    reader = open(filename)
    content = []

    path = reader.readline()
    while path is not None:
        path = path.split(";")
        content.append(path)
    reader.close()

    return content


def create_graph(node_file):
    nodes = {}
    for line in node_file:
        nodes[line[0]] = Node(line[0])
        nodes[line[2]] = Node(line[2])
    for line in node_file:
        nodes.get(line[0]).adjacencies.add(
                Edge(
                        nodes.get(line[2]),
                        float(line[1])
                )
        )
        nodes.get(line[2]).adjacencies.add(
                Edge(
                        nodes.get(line[0]),
                        float(line[1])
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
                node_queue.get(v)

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
