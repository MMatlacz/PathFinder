# -*- coding: utf-8 -*-
import json
from collections import defaultdict

import falcon

from Statics import getTemplate
from db_handler import get_all

template = getTemplate('index.html')

class Dijkstra(object):
    def __init__(self):
        pass


    def on_get(self, req, resp, start, finish):

        def prepare_string(string):
            new_string = string.decode('utf-8').lower()
            new_string = new_string[0].upper() + new_string[1:]
            return new_string.encode('utf-8')

        start = prepare_string(start)
        finish = prepare_string(finish)
        f = read_file('miasta-kopia.txt')
        graph = create_graph(f)
        visited, path = dijsktra(graph=graph, initial=start)
        city = path[finish]
        path1 = []
        path1.append(city)
        while city != str(start):
            city = path[city]
            path1.append(city)
        path1.reverse()
        path1.append(finish)
        path = []
        for p in path1:
            path.append(p.decode('utf-8'))
        response = {'start': start, 'finish': finish, 'distance': visited[finish], 'path': path1}
        resp.body = json.dumps(response)
        #resp.body = template.render(start=start.decode('utf-8'), finish = finish.decode('utf-8'), distance = visited[finish], path = path)
        #resp.content_type = 'text/html'
        resp.status = falcon.HTTP_200


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        if to_node not in self.edges[from_node]:
            self.edges[from_node].append(to_node)
        if from_node not in  self.edges[to_node]:
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
        path = line.split(";")
        content.append(path)
    return content


def create_graph(node_file):

    graph = Graph()
    '''
    for line in node_file:
        graph.add_node(line[0].strip())
        graph.add_node(line[2].strip())
        graph.add_edge(line[0].strip(), line[2].strip(), float(line[1]))
        graph.add_edge(line[2].strip(), line[0].strip(), float(line[1]))
    pprint(graph.nodes)
    pprint(graph.edges)
    '''
    #new version with db
    for line in get_all():
        start = line['start']
        finish = line['finish']
        distance = line['distance']
        graph.add_node(start)
        graph.add_node(finish)
        graph.add_edge(start, finish, distance=distance)
        graph.add_edge(finish, start, distance=distance)
    return graph
