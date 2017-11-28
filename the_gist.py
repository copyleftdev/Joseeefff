#!/usr/bin/env python

import fnmatch
import os
import sqlite3


# recursive lookup , pass the root directory and mask to  recieve a list of files.

def insert_record_as_processed(filename):
    conn = sqlite3.connect("db/memoize.db")
    cur = conn.cursor()
    try:
        q = "insert INTO processed (file_name) values('{}')".format(filename)
        cur.execute(q)
        conn.commit()
        conn.close()
    except Exception as e:
        pass

def fetch_all_processed_files():
    conn = sqlite3.connect("db/memoize.db")
    cur = conn.cursor()
    try:
        q = "select * from processed"
        cur.execute(q)
        data = cur.fetchall()
        column = 0
        conn.commit()
        conn.close()
        result = [elt[column] for elt in data]

        return result
    except Exception as e:
        pass


def collect_files(root_directory, file_mask):
    """ a recursive method to collect a list of files
       in a given root directory"""
    proceesed = fetch_all_processed_files()
    matches = []

    for root, dirnames, filenames in os.walk(root_directory):
        for filename in fnmatch.filter(filenames, file_mask):
            insert_record_as_processed(filename)
            for p in proceesed:
                boold = p in filename
                if boold is True:
                    pass
                elif "_" in filename:
                    matches.append(os.path.join(root, filename))
                else:
                    pass
    return matches



a = collect_files("test_data/","*.txt")
print a
