# -*- coding: utf-8 -*-
import csv, sys
import MySQLdb

from settings import db_user, db_passwd

class Docproduct(object):

    def __init__(self, limit=None):
        self.limit = limit

    def _query(self):
        db = MySQLdb.connect(host="192.168.2.131",
                           user=db_user,
                           passwd=db_passwd,
                           db='bifrost')

        limit_clause = ';'
        if self.limit:
            limit_clause = "LIMIT %s;" % (self.limit)

        cur = db.cursor()
        cur.execute("""SELECT productname,
                              manufacturername
                       FROM docproductinfo
                       %s""" % limit_clause)

        return cur.fetchall();

    def write_csv(self, filename):
        with open(filename + '.csv', 'wb') as f:
            w = csv.writer(f, delimiter=',',
                              quotechar="'",
                              quoting=csv.QUOTE_MINIMAL)
            for row in self._query():
                w.writerow(row)

if __name__ == "__main__":
    limit = None
    filename = 'test'
    if len(sys.argv) >= 3:
        limit = sys.argv[2]
    elif len(sys.argv) >= 2:
        filename = sys.argv[1]

    Docproduct(limit=limit).write_csv(filename)