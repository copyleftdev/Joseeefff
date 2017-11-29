#!/usr/bin/env python

import os

ROOT_FOLDER = 'test_data/'
FILE_EXT = '.txt'
proclog = ""

def collect_files(rf, fe):
    matches = []
    processed_files = set(line.strip() for line in open("pf.txt", 'r'))
    for root, dirnames, filenames in os.walk(rf):
        for filen in filenames:
            if filen.endswith(fe) and '_' in filen:
                if filen not in processed_files:
                    with open("pf.txt", 'a+') as log:
                        log.write(filen+"\n")
                        matches.append(os.path.join(root, filen))
    return matches


a = collect_files("test_data/", ".txt")
print a
