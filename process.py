import numpy as np

from person import Person

class Processor:
    def __init__(self, population: int = 1000, days: int = 365):
        self.population = population
        self.people = [Person() for _ in range(population)]
        self.people[0].infect()  # patient zero
        self.days = days

    def process(self):
        for day in range(self.days):
            meetings = 2 * self.population
            pairs = [np.random.choice(self.people, 2, replace=False)]
