import yaml
from itertools import cycle
import random
import numpy
import cv2

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
    
class Calendar:
    def __init__(self, states, initial_state, swap_prob, cycles, weeks, months):
        self.states = states
        self.initial_state = initial_state
        self.swap_probability = swap_prob
        self.cycles = cycles
        self.months = months
        self.weeks = weeks
        self.__states_cycle = CyclingStates(states,initial_state)

        self.state_changes = numpy.zeros(shape=(months,weeks,cycles))
        self.calendar = []

        for month in range(months):
            for week in range(weeks):
                for cycle in range(cycles):
                    self.state_changes[month][week][cycle] = self.__time_to_change(swap_prob)
                    if (self.state_changes[month][week][cycle]):
                        self.calendar.append(self.__states_cycle.next())
                        if (False):
                            print(f"Time to change! On month {month}, week {week} and cycle {cycle}")
                    else:
                        self.calendar.append(self.__states_cycle.current_state())
    
    def __time_to_change(self, swap_prob):
        return random.random() < swap_prob

def create_image_from_calendar(calendar, states_img_filelist, destination):
    assert len(calendar.states) == len(states_img_filelist), "The number of states of the calendar does not match the number of states of the image file list"

    final_res_x = 6000
    final_res_y = 6000

    loaded_images = []
    min_res_x = float('inf')
    min_res_y = float('inf')
    for state in states_img_filelist:
        _img = cv2.imread(state)
        height, width, _ = _img.shape
        min_res_x = min(min_res_x,width)
        min_res_y = min(min_res_y,height)
        loaded_images.append(_img)

    for img in loaded_images:
       height, width, _ = img.shape
       if width != min_res_x and height != min_res_y:
           img.resize(min_res_x,min_res_y)
           print(f"Resizing image")

    reduced_res_x = final_res_x//calendar.cycles
    reduced_res_y = final_res_y//calendar.weeks

    for month in range(calendar.months):
        y_start = 0
        y_end = reduced_res_y
        # create matrix of images
        canvas = numpy.zeros((final_res_x,final_res_y, 3), dtype=numpy.uint8)
        for week in range(calendar.weeks):
            x_start = 0
            x_end = reduced_res_x
            for cycle in range(calendar.cycles):
                index = cycle+week*calendar.cycles+month*calendar.weeks
                state_index = calendar.states.index(calendar.calendar[index])
                _img = numpy.zeros((reduced_res_x,reduced_res_y,3), dtype = numpy.uint8)
                _img = cv2.resize(loaded_images[state_index],(reduced_res_x,reduced_res_y))
                canvas[y_start:y_end, x_start:x_end] = _img
                x_start += reduced_res_x
                x_end += reduced_res_x
            y_start += reduced_res_y
            y_end += reduced_res_y
        cv2.imwrite(f"{destination.replace('.png',f"_month_{month:02}.png")}",canvas)

if __name__ == "__main__":
    # load calendar configuration from file and test if it is a good configuration
    calendar_configuration = yaml.safe_load(open("./cfg/configuration.yaml"))
    assert(calendar_configuration["initial_state"] in calendar_configuration["states"])
    calendar = Calendar(
        calendar_configuration["states"],
        calendar_configuration["initial_state"],
        eval(calendar_configuration["state_change_probability"]),
        calendar_configuration["cycles_per_week"],
        calendar_configuration["weeks_per_month"],
        calendar_configuration["months"]
        )
    if (calendar_configuration["create_calendar_image"]):
        create_image_from_calendar(calendar, ["./img/Day.jpg","./img/Night.jpg"], "./img/calendar.png")

    current_state = calendar_configuration["initial_state"]
    length_of_period = 0
    for cycle in calendar.calendar:
        length_of_period += 1
        if current_state != cycle:
            print(f"State Changed! This was the length of the {current_state} period {int(length_of_period/calendar_configuration["cycles_per_week"]//calendar_configuration["weeks_per_month"])} months {length_of_period//calendar_configuration["cycles_per_week"]} weeks and {length_of_period%calendar_configuration["cycles_per_week"]} cycles")
            current_state = cycle
            length_of_period = 0

