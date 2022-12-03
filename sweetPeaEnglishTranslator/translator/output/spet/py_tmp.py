from sweetpea import *
### REGULAR FACTORS
color = Factor("color",  ["red", "green"])
word = Factor("word", ["red", "green"])
### DERIVED FACTORS
##
def is_congruency_congruent(color, word):
    return color == word
def is_congruency_incongruent(color, word):
    return not is_congruency_congruent(color, word)
congruency = Factor("congruency", [DerivedLevel("congruent", WithinTrial(is_congruency_congruent, [color, word])), DerivedLevel("incongruent", WithinTrial(is_congruency_incongruent, [color, word]))])
##
def is_congruency_transition_repeat(congruency):
    return congruency[0] == congruency[-1]
def is_congruency_transition_switch(congruency):
    return not is_congruency_transition_repeat(congruency)
congruency_transition = Factor("congruency transition", [DerivedLevel("repeat", Transition(is_congruency_transition_repeat, [congruency])), DerivedLevel("switch", Transition(is_congruency_transition_switch, [congruency]))])
### EXPERIMENT
constraints = []
crossing = [color, word, congruency_transition]
design = [color, word, congruency, congruency_transition]
block = CrossBlock(design, crossing, constraints, require_complete_crossing=False)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments,"sweetPeaEnglishTranslator/translator/output/spet/seq_tmp")