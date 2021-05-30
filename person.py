from __future__ import annotations

import random
from enum import Enum
import numpy as np
from typing import Optional


class PolicyEnum(Enum):
    none = 'none'
    antigen = 'antigen'
    antigen_antibody = 'antigen_antibody'


class Person:
    def __init__(self,
                 strategy: PolicyEnum = PolicyEnum.none,
                 infection_probability: float = 0.1,
                 immunity_probability: float = 0.25):
        self.contagiousness = 0
        self.contagious_days: Optional[int] = None
        self.symptoms = False
        self.immunity = False
        self.immune_days: Optional[int] = None
        self.immunity_length = 180
        self.quarantined = False
        self.days_quarantined = None
        self.quarantine_length = 14
        self.knows_antibody = False
        self.knows_antibody_days = None
        self.strategy = strategy
        if random.uniform(0, 1) < infection_probability:
            self.infect()
        if random.uniform(0, 1) < immunity_probability:
            self.immunity = True
            self.immune_days = 0

    def infect(self):
        self.contagiousness = np.random.beta(a=5, b=7)
        self.contagious_days = 0
        self.symptoms = False

    def heal(self):
        self.contagiousness = 0
        self.contagious_days = None
        self.symptoms = False
        self.immunity = True
        self.immune_days = 0

    def is_infected(self):
        return self.contagiousness > 0

    def remove_immunity(self):
        self.immunity = False
        self.immune_days = None

    def test_antigen(self):
        if self.is_infected():
            self.quarantined = True
            self.days_quarantined = 0
            self.knows_antibody = True
            self.knows_antibody_days = 0

    def test_antibody(self):
        if self.contagious_days is not None and self.contagious_days > 8:
            self.quarantined = True
            self.days_quarantined = 0
            self.knows_antibody = True
            self.knows_antibody_days = 0
        elif self.immunity:
            self.knows_antibody = True
            self.knows_antibody_days = 0

    def meet_with_other(self, other: Person):
        if not self.contagiousness and \
                other.contagiousness and np.random.uniform() < other.contagiousness and not other.symptoms and not self.immunity:
            self.infect()
            return True

    def pass_day(self):
        if self.contagious_days is not None:
            self.contagious_days += 1
            if not self.symptoms and self.contagious_days == 5:
                self.symptoms = True
            elif self.contagious_days == 14:
                self.heal()
        if self.days_quarantined is not None:
            self.days_quarantined += 1
            if self.days_quarantined == self.quarantine_length:
                self.quarantined = False
                self.quarantine_length = None
        if self.knows_antibody_days is not None:
            self.knows_antibody_days += 1
            if self.knows_antibody_days == 170:
                self.knows_antibody = False
                self.knows_antibody_days = None
        if self.immunity and self.immune_days == self.immunity_length:
            self.remove_immunity()
        elif self.immunity:
            self.immune_days += 1
        if not self.immunity and random.uniform(0, 1) < 1 / 10000 and not self.is_infected():
            self.infect()
            return True
