from random import choice
from person import Person, PolicyEnum
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd


class Processor:
    def __init__(self,
                 population: int = 1000,
                 initial_infection_ratio: float = 0.001,
                 initial_immunity_ratio: float = 0.25,
                 days: int = 365,
                 strategy: PolicyEnum = PolicyEnum.none):
        self.budget = 0
        self.infection_count = 0
        self.population = population
        self.people = [Person(strategy=strategy,
                              infection_probability=initial_infection_ratio,
                              immunity_probability=initial_immunity_ratio)
                       for _ in range(population)]
        self.days = days
        self.strategy = strategy

    def process(self):
        counts = []
        for day in tqdm(range(self.days)):
            count = len([x for x in self.people if x.is_infected()])
            counts.append(count)
            meetings = int(0.5 * self.population)
            pairs = [(choice(self.people), choice(self.people)) for _ in range(meetings)]
            for person1, person2 in pairs:
                if person1 == person2:
                    continue
                if person1.quarantined or person2.quarantined:
                    continue
                p1infected = bool(person1.meet_with_other(person2))
                p2infected = bool(person2.meet_with_other(person1))
                self.infection_count += p1infected
                self.infection_count += p2infected
            if self.strategy == PolicyEnum.antigen:
                people_to_test = self.people[day % 14::14]
                [person.test_antigen() for person in people_to_test]
                self.budget += len(people_to_test) * 10
            elif self.strategy == PolicyEnum.antigen_antibody:
                people_with_no_antibody = [person for person in self.people if not person.knows_antibody]
                people_to_test_antigen = people_with_no_antibody[day % 14::14]
                people_to_test_antigen.extend([x for x in self.people if x.symptoms and not x.quarantined])
                [person.test_antigen() for person in people_to_test_antigen]
                self.budget += len(people_to_test_antigen) * 10
                people_with_no_antibody = [person for person in self.people if not person.knows_antibody]
                people_to_test_antibody = people_with_no_antibody[day % 60::60]
                [person.test_antigen() for person in people_to_test_antibody]
                self.budget += len(people_to_test_antibody) * 10

            for person in self.people:
                infected = bool(person.pass_day())
                self.infection_count += infected
        return counts, self.budget, self.infection_count


if __name__ == '__main__':
    population_range = [1000, 10000, 100000, 3000000]
    none_budgets = []
    antigen_budgets = []
    antigen_antibody_budgets = []
    none_counts = []
    antigen_counts = []
    antigen_antibody_counts = []
    for population_ in population_range:
        initial_infection_ratio_ = 0.001
        initial_immunity_ratio_ = 0.25
        processor = Processor(population=population_,
                              initial_infection_ratio=initial_infection_ratio_,
                              initial_immunity_ratio=initial_immunity_ratio_,
                              strategy=PolicyEnum.none)
        counts_none, budget_none, infection_count_none = processor.process()
        none_budgets.append(budget_none)
        none_counts.append(infection_count_none)
        plt.plot(counts_none, label="none")
        processor = Processor(population=population_,
                              initial_infection_ratio=initial_infection_ratio_,
                              initial_immunity_ratio=initial_immunity_ratio_,
                              strategy=PolicyEnum.antigen)
        counts_antigen, budget_antigen, infection_count_antigen = processor.process()
        antigen_budgets.append(budget_antigen)
        antigen_counts.append(infection_count_antigen)
        plt.plot(counts_antigen, label="antigen")
        processor = Processor(population=population_,
                              initial_infection_ratio=initial_infection_ratio_,
                              initial_immunity_ratio=initial_immunity_ratio_,
                              strategy=PolicyEnum.antigen_antibody)
        counts_antigen_antibody, budget_antigen_antibody, infection_count_antigen_antibody =\
            processor.process()
        antigen_antibody_budgets.append(budget_antigen_antibody)
        antigen_antibody_counts.append(infection_count_antigen_antibody)
        plt.plot(counts_antigen_antibody, label="antigen_antibody")
        plt.legend()
        plt.savefig(f"{population_}_people.png")
        plt.clf()
    df = pd.DataFrame(list(zip(none_budgets,
                               antigen_budgets,
                               antigen_antibody_budgets,
                               none_counts,
                               antigen_counts,
                               antigen_antibody_counts)), columns=[
        "none_budgets",
        "antigen_budgets",
        "antigen_antibody_budgets",
        "none_counts",
        "antigen_counts",
        "antigen_antibody_counts"])
    df.index = population_range

    df.to_csv('results.csv')
