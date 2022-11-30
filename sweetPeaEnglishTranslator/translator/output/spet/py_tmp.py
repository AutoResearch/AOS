from sweetpea.primitives import *
from sweetpea.constraints import *
from sweetpea import *
### REGULAR FACTORS
color = factor("color",  ["red", "green"])
word = factor("word", ["red", "green"])
task = factor("task", ["color naming", "word reading"])
### DERIVED FACTORS
##
def is_response_left(task, color, word):
    return (task == "color naming" and color == "red") or (task == "word reading" and word == "red")
def is_response_right(task, color, word):
    return not is_response_left(task, color, word)
response = factor("response", [derived_level("left", within_trial(is_response_left, [task, color, word])), derived_level("right", within_trial(is_response_right, [task, color, word]))])
##
def is_congruency_congruent(color, word):
    return color == word
def is_congruency_incongruent(color, word):
    return not is_congruency_congruent(color, word)
congruency = factor("congruency", [derived_level("congruent", within_trial(is_congruency_congruent, [color, word])), derived_level("incongruent", within_trial(is_congruency_incongruent, [color, word]))])
##
def is_task_transition_repetition(task):
    return task[0] == task[1]
def is_task_transition_switch(task):
    return not is_task_transition_repetition(task)
task_transition = factor("task transition", [derived_level("repetition", transition(is_task_transition_repetition, [task])), derived_level("switch", transition(is_task_transition_switch, [task]))])
### EXPERIMENT
constraints = [exclude(congruency, "congruent")]
crossing = [color, word, task]
design = [color, word, task, response, congruency, task_transition]
block = CrossBlock(design, crossing, constraints, require_complete_crossing=False)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments,"sweetPeaEnglishTranslator/translator/output/spet/seq_tmp")