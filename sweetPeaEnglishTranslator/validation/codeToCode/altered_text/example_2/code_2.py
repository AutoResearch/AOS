from sweetpea import *
### REGULAR FACTORS
letter = Factor("letter",  ["b", "f", "m", "q", "k", "x", "r", "h"])
### DERIVED FACTORS
##
def is_target_1(letter):
    return letter[0] == letter[-2]
def is_target_2(letter):
    return not is_target_1(letter)
target = Factor("target", [DerivedLevel(1, Window(is_target_1, [letter], 3, 1)), DerivedLevel(2, Window(is_target_2, [letter], 3, 1), 5)])
##
def is_one_back_1(letter):
    return letter[0] == letter[-1]
def is_one_back_2(letter):
    return not is_one_back_1(letter)
one_back = Factor("one back", [DerivedLevel(1, Window(is_one_back_1, [letter], 2, 1), 5), DerivedLevel(2, Window(is_one_back_2, [letter], 2, 1))])
##
def is_condi_1_1_0(letter):
    return letter[0] == letter[-2] and letter[0] != letter[-1]
def is_condi_1_2_0(letter):
    return letter[0] == letter[-2] and letter[0] == letter[-1]
def is_condi_2_1_0(letter):
    return letter[0] != letter[-2] and letter[0] != letter[-1]
def is_condi_2_2_0(letter):
    return letter[0] != letter[-2] and letter[0] == letter[-1]
condi = Factor("condi", [DerivedLevel("1/1/0", Window(is_condi_1_1_0, [letter], 3, 1), 3), DerivedLevel("1/2/0", Window(is_condi_1_2_0, [letter], 3, 1), 1), DerivedLevel("2/1/0", Window(is_condi_2_1_0, [letter], 3, 1), 17), DerivedLevel("2/2/0", Window(is_condi_2_2_0, [letter], 3, 1), 3)])
### EXPERIMENT
constraints = [MinimumTrials(48)]
crossing = [[letter, target], [one_back], [condi]]
design = [letter, target, one_back, condi]
block = MultiCrossBlock(design, crossing, constraints, require_complete_crossing=False)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments, 'code_2_sequences/seq')