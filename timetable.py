"""
A timetable interface created with python
"""
from collections import deque

import copy
import csv
import sys
import os

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time = ["9-12", "12-2"]
filename = "timetable.csv"


def read_timetable_from_csv(f=filename):
    with open(f, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def get_day(day):
    time_table = read_timetable_from_csv()
    for d in time_table:
        if d["day"] == day:
            return d


def save(time_table, *, fn=filename):
    print(time_table)
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=["day", *time])
        writer.writeheader()
        for row in time_table:
            writer.writerow(row)
    print("Time table saved successfully...")


def set_timetable():
    time_table = _set_timetable()
    save(time_table)


def _set_timetable():
    time_table = []
    for day in days:
        row = {"day": day}
        row.update({}.fromkeys(time, ""))
        tasks = input(
            f"Enter tasks for {day} seperated by semi-colon(;) (leave blank for a free period) : "
        ).split(";")
        task_queue = deque(tasks)
        for i in range(len(task_queue)):
            row[time[i]] = task_queue.popleft()
        time_table.append(row)
    return time_table


def _get_time_keys(timetable: list):
    # get only time keys
    for elem in copy.deepcopy(timetable):
        yield elem, elem.pop("day")


def _get_reset_params(day=None):
    if day == None:
        day = input("Enter day : ")
    time = input(
        "Enter time interval seperated by semi-colon (e.g 9-12; 12-2): "
    ).split(";")
    new_elem = {"day": day}
    for t in time:
        tasks = input(f"Enter tasks for {day}-{time} seperated by semi-colon(';') : ")
        new_elem.update({t: tasks})
    return new_elem


def reset_day(day: str) -> None:
    time_table = read_timetable_from_csv()
    new_elem = _get_reset_params(day)
    for t in time_table:
        if t["day"] == day:
            t.update(new_elem)
            break
    save(time_table)


def print_timetable(timetable):
    header = "{:^20}||".format("Day")
    # get only the time keys
    # we only need a loop
    # see if you can use reduce in itertools
    for time, _ in _get_time_keys(timetable):
        for t in time.keys():
            header += "{:^20}||".format(t)
        break
    # get each task for each day in each time allocation
    body = ""
    for time, day in _get_time_keys(timetable):
        body += "{:^20}||".format(day)
        for _, v in time.items():
            body += "{:^20}||".format(v)
        body += "\n"
    print(header + "\n" + body)


def view_timetable(f=filename):
    time_table = read_timetable_from_csv(f)
    print_timetable(time_table)


# if __name__ == "__main__":
#     set_timetable()
