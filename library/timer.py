# Console text colours
from collections import OrderedDict, deque
import json
from pathlib import Path
from statistics import mean
from time import perf_counter

WHITE = '\033[37m'
RED = '\033[91m'
GREEN = '\033[92m'


class Timer():
    """Class that allows easier timing of often repeated sections of code.
    This is by no means especially smart, but I couldn't find anything similar
    that is as easy to use."""

    __slots__ = ["start_times", "end_times", "indices", "average_of"]

    def __init__(self, average_of=200):
        self.start_times = {}
        self.end_times = OrderedDict()
        self.indeces = {}
        self.average_of = average_of

    def start(self, name):
        """Set the start time for this name"""
        self.start_times[name] = perf_counter()

    def stop(self, name):
        """Add an end time for this name"""
        time = perf_counter() - self.start_times[name]
        prev_times = self.end_times.get(name, deque(maxlen=self.average_of))

        prev_times.append(time)
        self.end_times[name] = prev_times
        self.indeces[name] = (self.indeces.get(name, 0) + 1) % self.average_of

    def next(self, stop_name, start_name):
        """Stop a timer and start another one."""
        self.stop(stop_name)
        self.start(start_name)

    def get_time(self, name):
        return mean(self.end_times[name])

    def get_total(self):
        return sum([mean(self.end_times[name]) for name in self.end_times.keys()])

    def print_average(self, name):
        average = mean(self.end_times[name])
        if self.indeces[name] >= self.average_of - 1:
            print(f"{name}: {' ' * (20 - len(name))}{average:.20f}")
        return average

    def sorted_dict(self) -> OrderedDict:
        items = sorted(self.end_times.items(), key=lambda i: mean(i[1]), reverse=True)
        return OrderedDict(items)

    def print_all(self, accuracy=6, print_sum=False):
        """Print all active timers with formatting.
        Accuracy is the number of decimal places to display"""
        string = ""
        sorted_dict = self.sorted_dict()
        for i, (k, v) in enumerate(sorted_dict.items()):
            if i == len(sorted_dict) - 1:
                color = GREEN
            elif i == 0:
                color = RED
            else:
                color = WHITE
            average = sum(v) if print_sum else mean(v)
            string += f"{color}{k}: {' ' * (20 - len(k))}{average:.{accuracy}f}\n"
        string += WHITE
        print(string)

    def export_json(self, file: Path, identifier: str):
        """Export the average times to a json file"""
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except (FileExistsError, json.JSONDecodeError):
            data = OrderedDict()

        data[identifier] = OrderedDict((key, mean(value)) for key, value in self.sorted_dict().items())

        with open(file, "w") as f:
            json.dump(data, f, indent=2)
