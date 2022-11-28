from sweetpea import *
from sweetpea.primitives import *
### REGULAR FACTORS
number = factor("number", [125, 132, 139, 146, 160, 167, 174, 181])
letter = factor("letter", ["b", "d", "f", "h", "s", "u", "w", "y"])
task = factor("task", ["number task", "letter task", "free choice task"])
### DERIVED FACTORS
##
def is_task_transition_forced_switch(task):
    return (task[1] == "number task" and task[0] == "letter task") or (task[1] == "letter task" and task[0] == "number task")
def is_task_transition_forced_repeat(task):
    return (task[1] == "number task" and task[0] == "number task") or (task[1] == "letter task" and task[0] == "letter task")
def is_task_transition_free_transition(task):
    return task[1] == "free choice task" and task[0] != "free choice task"
def is_task_transition_free_repeat(task):
    return task[1] == "free choice task" and task[0] == "free choice task"
def is_task_transition_forced_first(task):
    return task[1] != "free choice task" and task[0] == "free choice task"
task_transition = factor("task transition", [derived_level("forced switch", transition(is_task_transition_forced_switch, [task]), 3), derived_level("forced repeat", transition(is_task_transition_forced_repeat, [task])), derived_level("free transition", transition(is_task_transition_free_transition, [task]), 1), derived_level("free repeat", transition(is_task_transition_free_repeat, [task]), 1), derived_level("forced first", transition(is_task_transition_forced_first, [task]), 4)])
### EXPERIMENT
constraints = [minimum_trials(256)]
crossing = [[letter, number], [task_transition]]
design = [number, letter, task, task_transition]
block = MultiCrossBlock(design, crossing, constraints)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments, 'code_2_sequences/seq')