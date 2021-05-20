from __future__ import annotations

import numpy as np
from typing import Optional


class Person:
    def __init__(self):
        self.contagiousness = 0
        self.contagious_days: Optional[int] = None
        self.symptoms = False
        self.immunity = False
        self.immune_days: Optional[int] = None

    def infect(self):
        self.contagiousness = np.random.beta(a=6, b=6)
        self.contagious_days = 0
        self.symptoms = False

    def heal(self):
        self.contagiousness = 0
        self.contagious_days = None
        self.symptoms = False
        self.immunity = True
        self.immune_days = 0

    def remove_immunity(self):
        self.immunity = False
        self.immune_days = None

    def meet_with_other(self, other: Person):
        if not self.contagiousness and \
                other.contagiousness and np.random.uniform() < other.contagiousness:
            self.infect()

    def pass_day(self):
        if self.contagious_days is not None:
            self.contagious_days += 1
            if not self.symptoms and self.contagious_days == 5:
                self.symptoms = True
            elif self.contagious_days == 14:
                self.heal()
        if self.immunity and self.immune_days == 180:
            self.remove_immunity()
