from sweetpea import *
from sweetpea.primitives import *
### REGULAR FACTORS
letter = factor("letter",  ["b", "c", "d", "e"])
### DERIVED FACTORS
##
def is_target_1(letter):
    return letter[2] == letter[0]
def is_target_0(letter):
    return not is_target_1(letter)
target = factor("target", [derived_level(1, window(is_target_1, [letter], 3, 1), 2), derived_level(0, window(is_target_0, [letter], 3, 1), 3)])
### EXPERIMENT
constraints = []
crossing = [[letter, target]]
design = [letter, target]
block = MultiCrossBlock(design, crossing, constraints)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments, 'code_2_sequences/seq')