### REGULAR FACTORS
color   = factor("color", ["red", "green", "pink"])
word    = factor("word", ["red", "neutral", "blue"])
iti    = factor("iti", [300, 500])
### DERIVED FACTORS
##
def is_congruency_congruent(color, word):
  return color == word
def is_congruency_incongruent(color, word):
  return not is_congruency_congruent(color, word)
congruency = factor("congruency", [
  derived_level("congruent", within_trial(is_congruency_congruent, [color, word])),
  derived_level("incongruent", within_trial(is_congruency_incongruent, [color, word]))
])

##
def is_congruency_transition_switch(congruency):
  return congruency[0] != congruency[1]
def is_congruency_transition_repetition(congruency):
  return not is_congruency_transition_switch(congruency)
congruency_transition = factor("congruency transition", [
  derived_level("switch",
         transition(is_congruency_transition_switch, [congruency])),
  derived_level("repetition",
         transition(is_congruency_transition_repetition, [congruency]))
])

