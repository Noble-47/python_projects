"""
A timetable interface created with python
"""

from collections import deque
from rich.table import Table
from rich.console import Console

import random
import copy
import csv
import sys
import os


class Timetable:
    def __init__(self, filename=None):
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.time = ["9-12", "12-2", "8-10"]
        self.filename = filename or "timetable.csv"
        self._table = None

    def _read_timetable_from_csv(self):
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]

    def get_day(self, day):
        if not self._table:
            self._table = self._read_timetable_from_csv()
        for d in self._table:
            if d["day"] == day:
                return d

    def save(self):
        # print(self)
        with open(self.filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["day", *self.time])
            writer.writeheader()
            for row in self._table:
                writer.writerow(row)

    def set_timetable(self):
        self._table = self._set_timetable()
        self.save()

    def _set_timetable(self):
        time_table = []
        for day in self.days:
            row = {"day": day}
            row.update({}.fromkeys(self.time, ""))
            tasks = input(
                f"Enter tasks for {day} seperated by semi-colon(;) (leave blank for a free period) : "
            ).split(";")
            task_queue = deque(tasks)
            for i in range(len(task_queue)):
                row[time[i]] = task_queue.popleft()
            time_table.append(row)
        return time_table

    def _get_time_keys(self):
        # get only time keys
        if self._table == None:
            try:
                self._table = self._read_timetable_from_csv()
            except:
                raise Exception("Table was not set !!!")
        for elem in copy.deepcopy(self._table):
            yield elem, elem.pop("day")

    def _get_reset_params(self, day=None):
        time = input(
            "Enter time interval seperated by semi-colon (e.g 9-12; 12-2): "
        ).split(";")
        new_elem = {"day": day}
        for t in time:
            tasks = input(f"Enter tasks for {day}-{t} : ")
            new_elem.update({t: tasks})
        return new_elem

    def reset_day(self, day: list) -> None:
        if self._table is None:
            self._table = self._read_timetable_from_csv()
        time_table = self._table
        day_order = {'Monday' : 2, 'Tuesday'  : 3, 'Wednesday' : 4, 'Thursday' : 5, 'Friday' : 6, 'Saturday' : 7, 'Sunday' : 8}
        day_list = day[:] if len(day) == 1 else [day for day in sorted(day, key=lambda x : day_order.get(x))]
        for d in day_list:
            new_elem = self._get_reset_params(day)
            i = timetable.index(d)
            if timetable[i] == day:
                timetable[i].update(new_elem)
                break
        self.save()

    def print_table(self):
        table = Table(title='Timetable')
        colors = ['cyan', 'magenta', 'green', 'red', 'blue']
        for k in self._table[0]:
            table.add_column(k.title(), justify='right', style=random.choice(colors), no_wrap=True)
        # get each task for each day in each time allocation
        for time, day in self._get_time_keys():
            row = [day]
            for _, v in time.items():
                row.append(v)
            table.add_row(*row)
        console = Console()
        console.print(table)

    def load_table(self):
        self._table = self._read_timetable_from_csv()

    def view_day(self, days=None):
        if days:
            print(f"Day(s) : {[d for d in days]}")
            print("Haven't implemented that functionality yet")
            return
        if not self._table:
            self._table = self._read_timetable_from_csv()
        print(self)

    def __repr__(self):
        return 'Timetable object'
