from sweetpea.primitives import *
from sweetpea.constraints import *
from sweetpea import *
### REGULAR FACTORS
color = factor("color",  ["red", "green"])
word = factor("word", ["red", "green"])
### DERIVED FACTORS
##

def is_congruency_congruent(color, word):
    return color == word
def is_congruency_incongruent(color, word):
    return not is_congruency_congruent(color, word)
congruency = factor("congruency", [derived_level("congruent", within_trial(is_congruency_congruent, [color, word])), derived_level("incongruent", within_trial(is_congruency_incongruent, [color, word]))])
##
def is_congruency_transition_repeat(congruency):
    return congruency[0] == congruency[1]
def is_congruency_transition_switch(congruency):
    return not is_congruency_transition_repeat(congruency)
congruency_transition = factor("congruency transition", [derived_level("repeat", transition(is_congruency_transition_repeat, [congruency])), derived_level("switch", transition(is_congruency_transition_switch, [congruency]))])
### EXPERIMENT
constraints = []
crossing = [color, word, congruency_transition]
design = [color, word, congruency, congruency_transition]
block = CrossBlock(design, crossing, constraints)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments,"sweetPeaEnglishTranslator/translator/output/spet/seq_tmp")