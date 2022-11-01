import sys

sys.path.append("..")

from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition, Level
from sweetpea.constraints import at_most_k_in_a_row, minimum_trials
from sweetpea import fully_cross_block, synthesize_trials_non_uniform, print_experiments

### REGULAR FACTORS

object = Factor("object identity", [Level("H", 2), Level("S", 1)])
motion = Factor("motion", [Level("left", 2), Level("right", 3)])


### DERIVED FACTORS

## response factor

def response_left(object):
    return object == "H"


def response_right(object):
    return object == "S"


response = Factor("correct response", [
    DerivedLevel("left", WithinTrial(response_left, [object])),
    DerivedLevel("right", WithinTrial(response_right, [object])),
])


## congruency factor

def compatible(motion, response):
    return motion == response


def incompatible(motion, response):
    return not compatible(motion, response)


conLevel = DerivedLevel("compatible", WithinTrial(compatible, [motion, response]))
incLevel = DerivedLevel("incompatible", WithinTrial(incompatible, [motion, response]))

congruency = Factor("response congruency", [
    conLevel,
    incLevel
])


## congruency transition factor

def congr_repeat(congruency):
    return congruency[0] == congruency[1]


def congr_switch(congruency):
    return not congr_repeat(congruency)


congr_transition = Factor("congruency transition", [
    DerivedLevel("repeat", Transition(congr_repeat, [congruency])),
    DerivedLevel("switch", Transition(congr_switch, [congruency]))
])

### EXPERIMENT

# defining some constraints

constraints = [at_most_k_in_a_row(5, response),
               at_most_k_in_a_row(5, congruency),
               minimum_trials(100)]

# defining the counterbalancing scheme

design = [object, motion, congruency, response, congr_transition]
crossing = [object, motion, congr_transition]
block = fully_cross_block(design, crossing, constraints)

# solving for the experiment

experiments = synthesize_trials_non_uniform(block, 1)

### END OF EXPERIMENT DESIGN

print_experiments(block, experiments)
