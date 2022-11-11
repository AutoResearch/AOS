### REGULAR FACTORS
letter = factor("letter", ["A", "B", "C", "D", "E", "F"])

### DERIVED FACTORS
##
def is_target_yes(letter):
  return letter[0] == letter[3]
def is_target_no(letter):
  return not is_target_yes(letter)
target = factor("target", [
  derived_level("yes", window(is_target_yes, [letter], 4, 1)),
  derived_level("no", window(is_target_no, [letter], 4, 1))
])

##
def is_1back_lure_yes(letter):
  return letter[0] == letter[1]
def is_1back_lure_no(letter):
  return not is_1back_lure_yes(letter)
1back_lure = factor("1back lure", [
  derived_level("yes", window(is_1back_lure_yes, [letter], 3, 1)),
  derived_level("no", window(is_1back_lure_no, [letter], 3, 1))
])

##
def is_2back_lure_yes(letter):
  return letter[0] == letter[2]
def is_2back_lure_no(letter):
  return not is_2back_lure_yes(letter)
2back_lure = factor("2back lure", [
  derived_level("yes", window(is_2back_lure_yes, [letter], 3, 1)),
  derived_level("no", window(is_2back_lure_no, [letter], 3, 1))
])

##
def is_n_back_lure_yes(letter):
  return letter[0] == letter[1] or letter[0] == letter[2]
def is_n_back_lure_no(letter):
  return not is_n_back_lure_yes(letter)
n_back_lure = factor("n-back lure", [
  derived_level("yes", window(is_n_back_lure_yes, [letter], 3, 1)),
  derived_level("no", window(is_n_back_lure_no, [letter], 3, 1))
])

constraints = [minimum_trials(103)]
crossing = [target, n_back_lure]
design = [letter, target, 1back_lure, 2back_lure, n_back_lure]
block = fully_cross_block(design, crossing, constraints, False)
experiments = synthesize_trials_non_uniform(block, 1)
