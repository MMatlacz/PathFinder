# -*- coding: utf-8 -*-
import json
import sqlite3

import falcon

DATABASE = './database/connections.sqlite'
TABLE = 'connections'


def insert(start, destination, distance):
    return "INSERT into connections (start, finish, distance) VALUES ('{}', '{}', {})".format(start,
                                                                                              destination,
                                                                                              distance)


def update(start, finish, distance):
    return "UPDATE {} SET distance = {} WHERE start == '{}' AND finish == '{}'".format(TABLE,
                                                                                       distance,
                                                                                       start, finish)


# TODO: modify db queries to use sqlAlchemy
class Search:
    def on_get(self, req, resp):
        with connect_db() as db:
            query = "SELECT start FROM {}".format(TABLE)
            cities = db.cursor().execute(query).fetchall()
        data = []
        for city in cities:
            if city[0].encode('utf-8') not in data:
                data.append(city[0].encode('utf-8'))
        resp.body = json.dumps(data, encoding='utf-8')
        resp.status = falcon.HTTP_200


def connect_db():
    return sqlite3.connect(DATABASE, timeout=1)


# getting values from database
def get_from_db(*args):
    if len(args) == 1:
        try:
            with connect_db() as db:
                query = "SELECT start, finish, distance FROM {} WHERE ROWID == {}".format(TABLE, int(args[0]))
                return db.cursor().execute(query)
        except ValueError:
            print('Argument type error: expected integer got string')
            return -1
    elif len(args) == 2:
        with connect_db() as db:
            query = "SELECT id FROM {} WHERE start == '{}' AND finish == '{}'".format(TABLE, args[0], args[1])
            return db.cursor().execute(query)


# deleting from database - connection from start to finish gets deleted
def delete_from_db(start, finish):
    with connect_db() as db:
        query = "DELETE FROM {} WHERE start == '{}' AND finish == '{}'".format(TABLE, start, finish)
        db.cursor().execute(query)
        db.commit()


# get all connections between cities as list
def get_all():
    cities_raw = []
    with connect_db() as db:
        query = "SELECT start, finish, distance FROM connections"
        cities_raw = db.cursor().execute(query)
    cities = []
    for city in cities_raw.fetchall():
        start, finish, distance = city
        cities.append({'start': start.strip().encode('utf-8'), 'finish': finish.strip().encode('utf-8'),
                       'distance': float(distance)})
    return cities
