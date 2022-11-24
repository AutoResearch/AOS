from sweetpea import *
from sweetpea.primitives import *
### REGULAR FACTORS
letter = factor("letter",  ["b", "f", "m", "q", "k", "x", "r", "h"])
### DERIVED FACTORS
##
def is_target_1(letter):
    return letter[2] == letter[0]
def is_target_2(letter):
    return not is_target_1(letter)
target = factor("target", [derived_level("1", window(is_target_1, [letter], 3, 1)), derived_level("2", window(is_target_2, [letter], 3, 1), 5)])
##
def is_one_back_1(letter):
    return letter[0] != letter[1]
def is_one_back_2(letter):
    return not is_one_back_1(letter)
one_back = factor("one back", [derived_level("1", window(is_one_back_1, [letter], 2, 1), 5), derived_level("2", window(is_one_back_2, [letter], 2, 1))])
##
def is_condi_1_1_0(letter):
    return letter[2] == letter[0] and letter[2] != letter[1]
def is_condi_1_2_0(letter):
    return letter[2] == letter[0] and letter[2] == letter[1]
def is_condi_2_1_0(letter):
    return letter[2] != letter[0] and letter[2] != letter[1]
def is_condi_2_2_0(letter):
    return letter[2] != letter[0] and letter[2] == letter[1]
condi = factor("condi", [derived_level("1/1/0", window(is_condi_1_1_0, [letter], 3, 1), 3), derived_level("1/2/0", window(is_condi_1_2_0, [letter], 3, 1)), derived_level("2/1/0", window(is_condi_2_1_0, [letter], 3, 1), 17), derived_level("2/2/0", window(is_condi_2_2_0, [letter], 3, 1), 3)])
### EXPERIMENT
constraints = [minimum_trials(48)]
crossing = [[letter, target], [one_back], [condi]]
design = [letter, target, one_back, condi]
block = MultiCrossBlock(design, crossing, constraints)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGNsave_experiments_csv(block, experiments, 'code_2_sequences/seq')

experiment = synthesize_trials(block, 1)

save_experiments_csv(block, experiment, 'code_2_sequences/seq')