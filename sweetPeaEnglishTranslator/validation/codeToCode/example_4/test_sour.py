from sourpea import *
from sourpea.primitives import *
from sourpea.util import *

number_list = ["125", "132", "139", "146", "160", "167", "174", "181"]
letter_list = ['b', 'd', 'f', 'h', 's', 'u', 'w', 'y']

number = Factor("number", number_list)
letter = Factor("letter", letter_list)
task = Factor("task", ["number task", "letter task", "free choice task"])


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
    DerivedLevel("forced switch", Transition(is_forced_trial_switch, [task]), 3),
    DerivedLevel("forced repeat", Transition(is_forced_trial_repeat, [task])),
    DerivedLevel("free transition", Transition(is_free_trial_transition, [task]), 4),
    DerivedLevel("free repeat", Transition(is_free_trial_repeat, [task]), 4),
    DerivedLevel("forced first", Transition(is_not_relevant_transition, [task]), 4)
])
design = [letter, number, task, transit]
crossing = [[letter], [number], [transit]]
constraints = [MinimumTrials(256)]

block_1 = Block(design, [letter], constraints)
block_2 = Block(design, [number], constraints)
block_3 = Block(design, [transit], constraints)


sequence_1 = trials_from_csv('code_1_sequences/seq_0.csv')
sequence_2 = trials_from_csv('code_2_sequences/seq_0.csv')

for i in range(len(sequence_1)):
    sequence_1[i]['number'] = str(sequence_1[i]['number'])
    sequence_2[i]['number'] = str(sequence_2[i]['number'])

test_1 = block_1.test(sequence_1)
test_2 = block_2.test(sequence_1)
test_3 = block_3.test(sequence_1)

test_4 = block_1.test(sequence_2)
test_5 = block_2.test(sequence_2)
test_6 = block_3.test(sequence_2)


with open('scores.txt', 'w') as f:
    f.write('Original code, sourpea scores:\n')
    f.write(str(test_1) + '\n')
    f.write(str(test_2) + '\n')
    f.write(str(test_3) + '\n')
    f.write('Translated code, sourpea scores:\n')
    f.write(str(test_4) + '\n')
    f.write(str(test_5) + '\n')
    f.write(str(test_6) + '\n')