#!/bin/python3

import matplotlib.pyplot as plt
import json
import sys
from datetime import datetime
from collections import defaultdict
import pandas as pd
import numpy as np


def plot_weekdays(tasks_completed_at, fig=plt):
    dates = list(map(lambda e: datetime.fromtimestamp(e).weekday(), tasks_completed_at))
    weekdays = ["Mo", "Tue", "We", "Thu", "Fr", "Sa", "Su"]
    counts = { weekdays[i]: dates.count(i) for i in range(7) }
    fig.bar(counts.keys(), counts.values(), label='total number of tasks per weekday')
    fig.legend()


def plot_history(tasks_completed_at, fig=plt):
    # Count tasks at every day.
    tasks_by_date = defaultdict(lambda: 0)
    for t in tasks_completed_at:
        date = datetime.fromtimestamp(t)
        day = datetime(date.year, date.month, date.day)
        key = datetime.timestamp(day)
        tasks_by_date[key] += 1

    # Find range of dates.
    start_day = min(tasks_by_date.keys())
    end_day = max(tasks_by_date.keys())

    dates = pd.date_range(datetime.fromtimestamp(start_day), datetime.fromtimestamp(end_day), freq='1D').to_pydatetime().tolist()
    ntasks = [tasks_by_date[datetime.timestamp(d)] for d in dates]

    fig.bar(dates, ntasks, label='number of tasks per day')
    fig.axhline(np.mean(ntasks), color='orange', label='average number of tasks per day')
    fig.legend()


def main():
    tasks = json.load(sys.stdin)
    tasks_completed_at = [t["completed_at"] for t in tasks]
    history_fig = plt.subplot(1, 2, 1)
    weekday_fig = plt.subplot(1, 2, 2)
    plot_history(tasks_completed_at, history_fig)
    plot_weekdays(tasks_completed_at, weekday_fig)
    plt.show()


if __name__ == "__main__":
    main()
