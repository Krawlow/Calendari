import yaml
from itertools import cycle
import random
import numpy

def setup_cycle(states, initial_state):
    initial_state_of_cycle = states.index(initial_state)
    states_cycle = cycle(states)
    for i in range(initial_state_of_cycle):
        states_cycle.next()
    return states_cycle

def time_to_change(swap_prob):
    return random.random() < swap_prob

def create_calendar(states, initial_state, swap_prob, days, months, years):
    # set up the initial state of the cycle
    states_cycle = setup_cycle(states,initial_state)

    state_changes = numpy.zeros(shape=(years,months,days))

    for year in range(years):
        for month in range(months):
            for day in range(days):
                state_changes[year][month][day] = time_to_change(swap_prob)
                if (state_changes[year][month][day]):
                    print(f"Time to change! On year {year}, month {month} and day {day}")


    return state_changes


    

if __name__ == "__main__":
    # load calendar configuration from file and test if it is a good configuration
    calendar_configuration = yaml.safe_load(open("./cfg/configuration.yaml"))
    assert(calendar_configuration["initial_state"] in calendar_configuration["states"])
    calendar = create_calendar(
        calendar_configuration["states"],
        calendar_configuration["initial_state"],
        eval(calendar_configuration["state_change_probability"]),
        calendar_configuration["days_per_month"],
        calendar_configuration["months_per_year"],
        calendar_configuration["years"]
        )

