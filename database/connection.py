import os, psycopg2, json

class Connection(object):

    _db_connection = None
    _db_cur = None

    def __init__(self, dbname, host, port, username, password):
        self._db_connection = psycopg2.connect(dbname=dbname, host=host, port=port, user=username, password=password)
        self._db_cur = self._db_connection.cursor()

    def query(self, dbschema, query):
        self._db_cur.execute("SET search_path TO %s,public;" % (dbschema) + query)
        return self._db_cur.fetchall()

    def __del__(self):
        self._db_connection.close()
