# -*- coding: utf-8 -*-
import json
import sqlite3

import falcon

DATABASE = './database/connections.sqlite'
TABLE = 'connections'


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
        print(resp.body)
        resp.status = falcon.HTTP_200


class Modify:
    def __init__(self):
        self.msg = 'modification successful'

    def on_post(self, req, resp, start, finish, distance):
        if not get_from_db(start, finish).fetchall():
            with connect_db() as db:
                query = "INSERT into connections (start, finish, distance) VALUES ('{}', '{}', {})".format(start,
                                                                                                           finish,
                                                                                                           distance)
                db.cursor().execute(query)
                db.commit()

    def on_delete(self, req, resp, start, finish):
        delete_from_db(start, finish)
        resp.body = json.dumps(self.msg)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, start, finish, distance):
        with connect_db() as db:
            query = "UPDATE {} SET distance = {} WHERE start == '{}' AND finish == '{}'".format(TABLE,
                                                                                                distance,
                                                                                                start, finish)
            db.cursor().execute(query)
            db.commit()
        resp.body = json.dumps(self.msg)
        resp.status = falcon.HTTP_200


def connect_db():
    return sqlite3.connect(DATABASE, timeout=1)


# getting values from database
def get_from_db(*args):
    if len(args) == 1:
        try:
            with connect_db() as db:
                query = "SELECT start, finish, distance FROM {} WHERE ID == {}".format(TABLE, int(args[0]))
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
    def get_number_of_elements():
        with connect_db() as db:
            query = "SELECT COUNT( id ) FROM {}".format(TABLE)
            number = db.cursor().execute(query)
            return int(number.fetchone()[0])

    cities = []
    for i in range(1, get_number_of_elements()):
        con = get_from_db(i)
        start, finish, distance = con.fetchall()[0]
        cities.append({'start': start.strip().encode('utf-8'), 'finish': finish.strip().encode('utf-8'),
                       'distance': float(distance)})
    return cities
