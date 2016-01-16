# -*- coding: utf-8 -*-
import json
from collections import defaultdict

import falcon

from db_handler import get_all, get_from_db, connect_db, delete_from_db, insert, update


class Path:
    def __init__(self):
        self.msg = 'modification successful'

    def on_get(self, req, resp, start, finish):

        start = prepare_string(start)
        finish = prepare_string(finish)
        graph = create_graph()
        visited, paths = dijkstra(graph=graph, initial=start)
        print(paths)
        city = paths[finish]
        path = [city]
        while city != str(start):
            city = paths[city]
            path.append(city)
        path.reverse()
        path.append(finish)
        path_formatted = []
        for p in path:
            path_formatted.append(p.decode('utf-8'))
        response = {'start': start, 'finish': finish, 'distance': round(visited[finish], 2), 'path': path_formatted}
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, start, finish, distance):
        if not get_from_db(start, finish).fetchall():
            with connect_db() as db:
                query = insert(start, finish, distance)
                db.cursor().execute(query)
                db.commit()
        resp.body = json.dumps(self.msg)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, start, finish):
        delete_from_db(start, finish)
        delete_from_db(finish, start)
        resp.body = json.dumps(self.msg)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, start, destination, distance):
        with connect_db() as db:
            query = update(start, destination, distance)
            db.cursor().execute(query)
            db.commit()
        resp.body = json.dumps(self.msg)
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
        if from_node not in self.edges[to_node]:
            self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
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


def create_graph():
    """

    :rtype: Graph
    """
    graph = Graph()

    for line in get_all():
        start = line['start']
        finish = line['finish']
        distance = line['distance']
        graph.add_node(start)
        graph.add_node(finish)
        graph.add_edge(start, finish, distance=distance)
        graph.add_edge(finish, start, distance=distance)
    return graph


def prepare_string(string):
    """

    :param string:
    :rtype: str
    """
    string = string.split(' ')
    new_string = ''
    for elem in string:
        new_elem = elem.decode('utf-8').lower()
        new_elem = new_elem[0].upper() + new_elem[1:]
        new_string += new_elem + ' '

    new_string = new_string.strip()
    return new_string.encode('utf-8')
