
### REGULAR FACTORS
number_list = [125, 132, 139, 146, 160, 167, 174, 181]
letter_list = ['b', 'd', 'f', 'h', 's', 'u', 'w', 'y']
number = Factor("number", number_list)
letter = Factor("letter", letter_list)
task = Factor("task", ["number task", "letter task", "free choice task"])
### DERIVED FACTORS
##
def is_forced_trial_switch(task):
    return (task[0] == "number task" and task[1] == "letter task") or \
           (task[0] == "letter task" and task[1] == "number task")
def is_forced_trial_repeat(task):
    return (task[0] == "number task" and task[1] == "number task") or \
           (task[0] == "letter task" and task[1] == "letter task")
def is_free_trial_transition(task):
    return task[0] != "free choice task" and task[1] == "free choice task"
def is_free_trial_repeat(task):
    return task[0] == "free choice task" and task[1] == "free choice task"
def is_not_relevant_transition(task):
    return not (is_forced_trial_repeat(task) or is_forced_trial_switch(task) or is_free_trial_repeat(
        task) or is_free_trial_transition(task))
transit = Factor("task transition", [
    DerivedLevel("forced switch", transition(is_forced_trial_switch, [task]), 3),
    DerivedLevel("forced repeat", transition(is_forced_trial_repeat, [task])),
    DerivedLevel("free transition", transition(is_free_trial_transition, [task]), 4),
    DerivedLevel("free repeat", transition(is_free_trial_repeat, [task]), 4),
    DerivedLevel("forced first", transition(is_not_relevant_transition, [task]), 4)
])
### EXPERIMENT
design = [letter, number, task, transit]
crossing = [[letter], [number], [transit]]
constraints = [MinimumTrials(256)]
block = MultiCrossBlock(design, crossing, constraints)
experiment = synthesize_trials(block, 1)
save_experiments_csv(block, experiment, 'code_1_sequences/seq')
### END OF EXPERIMENT DESIGN
