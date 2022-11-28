import sourpea.util
from sourpea import *
from sourpea.primitives import *
from sourpea.util import *

color = Factor('color', ['red', 'green', 'blue', 'yellow'])
word = Factor('word', ['red', 'green', 'blue', 'yellow'])

def is_congruent(word, color):
    return word == color
def is_not_congruent(word, color):
    return not is_congruent(word, color)

congruent = DerivedLevel('congruent', DerivationWindow(is_congruent, [word, color]))
incongruent = DerivedLevel('incongruent', DerivationWindow(is_not_congruent, [word, color]))

congruency = Factor('congruency', [congruent, incongruent])

constraints = [MinimumTrials(48)]
design = [word, color, congruency]
crossing = [word, congruency]

block = Block(design=design, crossing=crossing, constraints=constraints)

sequence_1 = trials_from_csv('code_1_sequences/seq_0.csv')
sequence_2 = trials_from_csv('code_2_sequences/seq_0.csv')


test_1 = block.test(sequence_1)
test_2 = block.test(sequence_2)

with open('scores.txt', 'w') as f:
    f.write('Original code, sourpea scores:\n')
    f.write(str(test_1) + '\n')
    f.write('Translated code, sourpea scores:\n')
    f.write(str(test_2) + '\n')

