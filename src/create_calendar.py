import yaml
from itertools import cycle
import random
import numpy

class CyclingStates:
    def __init__(self, states, initial):
        if initial not in states:
            raise ValueError("Initial state must be in the list of states")
        self.states = states
        self.index = self.states.index(initial)
    
    def next(self):
        self.index = (self.index +1) % len(self.states)
        return self.states[self.index]
    
    def current_state(self):
        return self.states[self.index]

def time_to_change(swap_prob):
    return random.random() < swap_prob

def create_calendar(states, initial_state, swap_prob, cycles, weeks, months):
    # set up the initial state of the cycle
    states_cycle = CyclingStates(states,initial_state)

    state_changes = numpy.zeros(shape=(months,weeks,cycles))
    calendar = []

    for month in range(months):
        for week in range(weeks):
            for cycle in range(cycles):
                state_changes[month][week][cycle] = time_to_change(swap_prob)
                if (state_changes[month][week][cycle]):
                    calendar.append(states_cycle.next())
                    if (False):
                        print(f"Time to change! On month {month}, week {week} and cycle {cycle}")
                else:
                    calendar.append(states_cycle.current_state())
    return calendar

if __name__ == "__main__":
    # load calendar configuration from file and test if it is a good configuration
    calendar_configuration = yaml.safe_load(open("./cfg/configuration.yaml"))
    assert(calendar_configuration["initial_state"] in calendar_configuration["states"])
    calendar = create_calendar(
        calendar_configuration["states"],
        calendar_configuration["initial_state"],
        eval(calendar_configuration["state_change_probability"]),
        calendar_configuration["cycles_per_week"],
        calendar_configuration["weeks_per_month"],
        calendar_configuration["months"]
        )
    current_state = calendar_configuration["initial_state"]
    length_of_period = 0
    for cycle in calendar:
        length_of_period += 1
        if current_state != cycle:
            print(f"State Changed! This was the length of the {current_state} period {int(length_of_period/calendar_configuration["cycles_per_week"]//calendar_configuration["weeks_per_month"])} months {length_of_period//calendar_configuration["cycles_per_week"]} weeks and {length_of_period%calendar_configuration["cycles_per_week"]} cycles")
            current_state = cycle
            length_of_period = 0

