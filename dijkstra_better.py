#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijsktra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


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

    graph = Graph()

    for line in node_file:
        graph.add_node(line[0].strip())
        graph.add_node(line[2].strip())
        graph.add_edge(line[0].strip(), line[2].strip(), float(line[1]))
        graph.add_edge(line[2].strip(), line[0].strip(), float(line[1]))

    return graph

f = read_file(sys.argv[1])
graph = create_graph(f)
visited, path = dijsktra(graph=graph, initial=sys.argv[2])
print(path)
print(visited["Łódź"])

