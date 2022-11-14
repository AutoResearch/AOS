from sweetpea.primitives import *
from sweetpea.constraints import *
from sweetpea import *
### REGULAR FACTORS
letter = factor("letter", ["a", "b", "c", "d", "e", "f"])
### DERIVED FACTORS
##
def is_target_yes(letter):
    return letter[0] == letter[3]
def is_target_no(letter):
    return not is_target_yes(letter)
target = factor("target", [
    derived_level("yes", window(is_target_yes, [letter], 4, 1)),
    derived_level("no",  window(is_target_no, [letter], 4, 1))
])
##
def is_one_back_lure_yes(letter):
    return letter[0] == letter[1]
def is_one_back_lure_no(letter):
    return not is_one_back_lure_yes(letter)
one_back_lure = factor("one-back lure", [
    derived_level("yes", window(is_one_back_lure_yes, [letter], 3, 1)),
    derived_level("no",  window(is_one_back_lure_no, [letter], 3, 1))
])
##
def is_two_back_lure_yes(letter):
    return letter[0] == letter[2]
def is_two_back_lure_no(letter):
    return not is_two_back_lure_yes(letter)
two_back_lure = factor("two-back lure", [
    derived_level("yes", window(is_two_back_lure_yes, [letter], 3, 1)),
    derived_level("no",  window(is_two_back_lure_no, [letter], 3, 1))
])
##
def is_n_back_lure_yes(letter):
    return letter[0] == letter[1] or letter[0] == letter[2]
def is_n_back_lure_no(letter):
    return not is_n_back_lure_yes(letter)
n_back_lure = factor("n-back lure", [
    derived_level("yes", window(is_n_back_lure_yes, [letter], 3, 1)),
    derived_level("no",  window(is_n_back_lure_no, [letter], 3, 1))
])
### EXPERIMENT
constraints = [minimum_trials(103)]
crossing = [target, n_back_lure]
design = [letter, target, one_back_lure, two_back_lure, n_back_lure]
block = fully_cross_block(design, crossing, constraints, False)
experiments = synthesize_trials_non_uniform(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments,"sweetPeaEnglishTranslator/translator/output/seq_tmp")