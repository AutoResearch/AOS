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
def is_lure_yes(letter):
  return letter[0] == letter[1] or letter[0] == letter[2]
def is_lure_no(letter):
  return not is_lure_yes(letter)
lure = factor("lure", [
  derived_level("yes", window(is_lure_yes, [letter], 3, 1)),
  derived_level("no", window(is_lure_no, [letter], 3, 1))
])

constraints = []
crossing = [target, lure]
design = [letter, target, lure]
block = fully_cross_block(design, crossing, constraints, False)
experiments = synthesize_trials_non_uniform(block, 1)
