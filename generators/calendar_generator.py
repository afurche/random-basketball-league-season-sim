from itertools import permutations
from random import shuffle
from pandas import date_range


class CalendarGenerator:

    @classmethod
    def create_calendar(cls):
        combs = [tup for tup in permutations(range(10), 2)]
        shuffle(combs)
        dates = [i.date() for i in date_range("2020-01-01", periods=len(combs))]

        return [(date, comb) for date, comb in zip(dates, combs)]


