import sqlite3
import logging
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
from copy import deepcopy


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("covid")


db = "/mnt/c/Users/ian/Documents/git/keep/covid.db"
db = r"C:\Users\ian\Documents\git\keep\covid.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

data = cursor.execute("SELECT * from covid").fetchall()

# (1612742400, '2021-02-08', 826, 26470, 3.12)
Line = namedtuple("Line", ["date", "human_date", "cases", "tests", "percentage"])
lines = []
for i in data:
    lines.append(Line(*i))

dates = []
human_dates = []
cases = []
tests = []
percentage = []

for line in lines:
    dates.append(line.date)
    human_dates.append(line.human_date)
    cases.append(line.cases)
    tests.append(line.tests)
    percentage.append(line.percentage)

cases_d_100 = list(map(lambda x: x / 100, iter(cases)))
tests_d_1000 = list(map(lambda x: x / 1000, iter(tests)))


def seven_day_average(li):
    li_ave = []
    cli = deepcopy(li)
    while len(cli) >= 7:
        group = cli[0:6]
        avg = sum(group) / 7
        li_ave.append(round(avg, 2))
        del cli[0]
    return li_ave


week_ave_cases = seven_day_average(cases)
week_ave_cases = list(map(lambda x: x / 100, iter(week_ave_cases)))
week_ave_tests = seven_day_average(tests)
week_ave_tests = list(map(lambda x: x / 1000, iter(week_ave_tests)))
week_ave_percent = seven_day_average(percentage)


plt.xlabel("Date")
plt.xticks(rotation=45)
plt.yticks(range(0, int(max(tests_d_1000)) + 1))
plt.plot(
    human_dates,
    tests_d_1000,
    label="Tests div 1000",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)
plt.plot(
    human_dates,
    cases_d_100,
    label="Cases div 100",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)
plt.plot(
    human_dates,
    percentage,
    label="Percent positive",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)
plt.plot(
    human_dates[:-6],
    week_ave_cases,
    label="Cases - 7 day average",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)
plt.plot(
    human_dates[:-6],
    week_ave_tests,
    label="Tests - 7 day average",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)
plt.plot(
    human_dates[:-6],
    week_ave_percent,
    label="Percent positive - 7 day average",
    marker="o",
    markerfacecolor="black",
    markersize=2,
)

plt.legend()
plt.grid(axis="y", linewidth=0.5)
plt.show()
