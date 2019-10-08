# -*- coding: iso-8859-1 -*-
""" This module aims to compare 2 DB and check for differences.
    As it uses memory to compare table content, it may not be the right tool for huge tables.
    comparison will output every different record (and will take longer to run)
"""
import os
import pprint

import psycopg2


class Parameters:

    def __init__(self, name1, host1, port1, user1, password1, name2, host2, port2, user2, password2, tables,
                 name_check, complete, right_to_left, output_path):
        self.db1prms = {"host": host1 + ":" + port1, "user": user1, "passwd": password1, "db": name1}
        self.db2prms = {"host": host2 + ":" + port2, "user": user2, "passwd": password2, "db": name2}

        self.db1 = psycopg2.connect(user=user1,
                                    password=password1,
                                    host=host1,
                                    port=port1,
                                    database=name1)

        self.db2 = psycopg2.connect(user=user2,
                                    password=password2,
                                    host=host2,
                                    port=port2,
                                    database=name2)

        self.tables = tables
        self.name_check = name_check
        self.complete_check = complete
        self.right_to_left_check = right_to_left
        self.outpath = output_path


class DbOperator(object):
    """ Utilities to interact with database
    """

    def __init__(self, db, name=''):
        self.db = db
        self.name = name
        self.cur = db.cursor()

    def get_rows(self, tbl):
        """ Returns the content of the table tbl
        """
        statmt = "select * from %s" % tbl
        self.cur.execute(statmt)
        rows = list(self.cur.fetchall())
        return rows

    def get_table_list(self, tables):
        """ Returns the list of the DB tables
        """
        statmt = "SELECT tablename FROM pg_catalog.pg_tables where tablename not like 'pg_%' and tablename not like 'sql_%'"
        self.cur.execute(statmt)
        rows = [table[0] for table in list(self.cur.fetchall())]

        if len(tables) != 0:
            rows = list(map(str, set(rows).intersection(tables)))
        return rows


def tuple_to_string(tup):
    return map(str, tup)


def tuple_to_single_line(tup_str):
    return '    '.join(tuple_to_string(tup_str))


def prettify_and_list(param):
    return list(map(tuple_to_single_line, param))


def compare_lists(l1, l2):
    result = {'l1notInl2': [],
              'l2notInl1': []}
    d1 = dict(zip(l1, l1))
    d2 = dict(zip(l2, l2))
    for row in l1:
        if not row in d2:
            result['l1notInl2'].append(row)
    for row in l2:
        if not row in d1:
            result['l2notInl1'].append(row)
    return result


class DbCompare(object):
    """ Core function to compare the DBs
    """

    def __init__(self, params):
        self.params = params

    def process(self):

        if self.params.outpath:
            output_location = self.params.outpath + "/"
        else:
            output_location = self.params.outpath

        of = OutFile(output_location + "tables.txt")

        db1 = DbOperator(self.params.db1, self.params.db1prms["host"])
        db2 = DbOperator(self.params.db2, self.params.db2prms["host"])
        tl1 = db1.get_table_list(self.params.tables)
        tl2 = db2.get_table_list(self.params.tables)

        if self.params.name_check or self.params.complete_check:
            if tl1 == tl2:
                of.write("Identical tables")

        else:
            print("Different tables")
            of.write("Different tables")
            cp = compare_lists(tl1, tl2)
            if cp['l1notInl2']:
                of.write("   --> Tables from %s missing in %s" % (db1.name, db2.name))
                of.write("\n".join([t[0] for t in cp['l1notInl2']]))
            if cp['l2notInl1']:
                of.write("   --> Tables from %s missing in %s" % (db2.name, db1.name))
                of.write(",".join([t[0] for t in cp['l2notInl1']]))

        for tbl in tl1:
            if tbl in tl2:
                print(tbl)
                of.write(tbl)
                out = OutFile(output_location + tbl)
                rl1 = db1.get_rows(tbl)
                rl2 = db2.get_rows(tbl)
                if rl1 == rl2:
                    out.write("--> %s identical \n" % tbl)
                else:
                    out.write("\nSHOWING DIFFERENCES IN : %s" % tbl)

                    cp = compare_lists(rl1, rl2)

                    out.write("\nShowing DB1 content that is not in DB2")
                    if cp['l1notInl2']:
                        out.write("\n".join(prettify_and_list(cp['l1notInl2'])))

                    if self.params.right_to_left_check or self.params.complete_check:
                        of.write("\nShowing DB2 content that is not in DB1")
                        if cp['l2notInl1']:
                            out.write("\n".join(prettify_and_list(cp['l2notInl1'])))


class OutFile(object):
    """ To write in the outfile
    """

    def __init__(self, fileout):
        self.outFile = fileout
        os.makedirs(os.path.dirname(self.outFile), exist_ok=True)
        df = open(self.outFile, 'w')
        df.close()

    def write(self, *msg):

        df = open(self.outFile, 'a')
        for m in msg:
            if type(m) is dict or type(m) is list:
                df.write("%s\n" % pprint.pformat(m))
            else:
                df.write("%s\n" % str(m))
            df.close()
