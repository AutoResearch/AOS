from sweetpea import *

color = Factor('color', ['red', 'green', 'blue', 'yellow'])
word = Factor('word', ['red', 'green', 'blue', 'yellow'])

def is_congruent(word, color):
    return (word == color)

def is_not_congruent(word, color):
    return not is_congruent(word, color)

congruent = DerivedLevel('congruent', WithinTrial(is_congruent, [word, color]))
incongruent = DerivedLevel('incongruent', WithinTrial(is_not_congruent, [word, color]))

congruency = Factor('congruency', [congruent, incongruent])

constraints = [MinimumTrials(48)]
design = [word, color, congruency]
crossing = [word, congruency]

block = CrossBlock(design, crossing, constraints)

experiment = synthesize_trials(block, 1)

save_experiments_csv(block, experiment, 'code_1_sequences/seq')