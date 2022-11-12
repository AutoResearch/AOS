from sweetpea.primitives import *
from sweetpea.constraints import *
from sweetpea import *
### REGULAR FACTORS
iti = factor("iti", ["long", "short"])
length = factor("length", ["long", "short"])
### DERIVED FACTORS
##
def is_alignment_aligned(length, iti):
    return length == iti
def is_alignment_unaligned(length, iti):
    return not is_alignment_aligned(length, iti)
alignment = factor("alignment", [
    derived_level("aligned", within_trial(is_alignment_aligned, [length, iti])),
    derived_level("unaligned", within_trial(is_alignment_unaligned, [length, iti]))
])
##
def is_alignment_transition_aligned(length, iti):
    return length[0] == iti[1]
def is_alignment_transition_unaligned(length, iti):
    return not is_alignment_transition_aligned(length, iti)
alignment_transition = factor("alignment transition", [
    derived_level("aligned", transition(is_alignment_transition_aligned, [length, iti])),
    derived_level("unaligned", transition(is_alignment_transition_unaligned, [length, iti]))
])
constraints = [exclude(alignment_transition, "unaligned")]
crossing = [iti, length, alignment, alignment_transition]
### EXPERIMENT
design = [iti, length, alignment, alignment_transition]
block = fully_cross_block(design, crossing, constraints, False)
experiments = synthesize_trials_non_uniform(block, 1)
### END OF EXPERIMENT DESIGN