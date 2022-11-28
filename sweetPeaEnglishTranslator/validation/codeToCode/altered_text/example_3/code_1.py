from sweetpea import *
from sweetpea.primitives import *
from sweetpea.constraints import *

letter = Factor('letter', ['b', 'c', 'd', 'e'])

def is_target(letter):
    return letter[0] == letter[2]
def is_not_target(letter):
    return not is_target(letter)

target_true = DerivedLevel(1, window(is_target, [letter], 3, 1), 2)
target_false = DerivedLevel(0, window(is_not_target, [letter], 3, 1), 3)

target = Factor('target', [target_true, target_false])


block = CrossBlock([letter, target], [letter, target], [])

experiment = synthesize_trials(block, 1)

save_experiments_csv(block, experiment, 'code_1_sequences/seq')