#!/usr/bin/env python

import requests
import csv
from io import StringIO
import sqlite3
from datetime import datetime
import re
import logging
import sys


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("covid")


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def process_line(x):
    date = int((datetime.strptime(x[0], p) - epoch).total_seconds())
    human_date = x[0]
    try:
        cases = int(re.sub("[^0-9]+", "", x[1]))
    except ValueError:
        cases = "NA"
    try:
        tests = int(re.sub("[^0-9]+", "", x[-2]))
    except ValueError:
        tests = "NA"
    try:
        percentage = truncate((cases / tests) * 100, 2)
    except TypeError:
        percentage = "NA"
    return date, human_date, cases, tests, percentage


p = "%Y-%m-%d"
epoch = datetime(1970, 1, 1)


db = "/mnt/c/Users/ian/Documents/git/keep/covid.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

try:
    cursor.execute(
        "CREATE TABLE covid (date INTEGER PRIMARY KEY, human_date TEXT, cases INTEGER, tests INTEGER, percentage REAL)"
    )
except sqlite3.OperationalError:
    pass

url = "https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/synthese-7jours.csv"

content = requests.get(url, allow_redirects=True).content.decode("UTF-8")

c = csv.reader(StringIO(content.strip("\r")), delimiter=";")
next(c)

for x in c:
    line = process_line(x)
    sline = str(line)
    if line[-1] != "NA":
        log.debug(f"inserting: {sline}")
        cursor.execute(f"REPLACE INTO covid VALUES {sline}")
    else:
        log.debug(f"discard: {sline}")

connection.commit()
# rows = cursor.execute("SELECT * FROM covid").fetchall()
# print(rows)

