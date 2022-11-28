from sweetpea import *
from sweetpea.primitives import *
### REGULAR FACTORS
color = factor("color",  ["red", "green", "blue", "yellow"])
word = factor("word", ["red", "green", "blue", "yellow"])
### DERIVED FACTORS
##
def is_congruency_congruent(word, color):
    return word == color
def is_congruency_incongruent(word, color):
    return not is_congruency_congruent(word, color)
congruency = factor("congruency", [derived_level("congruent", within_trial(is_congruency_congruent, [word, color])), derived_level("incongruent", within_trial(is_congruency_incongruent, [word, color]))])
### EXPERIMENT
constraints = [minimum_trials(48)]
crossing = [[word, congruency]]
design = [color, word, congruency]
block = MultiCrossBlock(design, crossing, constraints)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments, 'code_2_sequences/seq')