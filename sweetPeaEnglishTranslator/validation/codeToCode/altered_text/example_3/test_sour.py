from sourpea import *
from sourpea.primitives import *
from sourpea.util import *

letter = Factor('letter', ['b', 'c', 'd', 'e'])

def is_target(letter):
    return letter[0] == letter[2]
def is_not_target(letter):
    return not is_target(letter)

target_true = DerivedLevel(1, DerivationWindow(is_target, [letter], 3), 2)
target_false = DerivedLevel(0, DerivationWindow(is_not_target, [letter], 3), 3)

target = Factor('target', [target_true, target_false])


block = Block([letter, target], [letter, target], [])

sequence_1 = trials_from_csv('code_1_sequences/seq_0.csv')
sequence_2 = trials_from_csv('code_2_sequences/seq_0.csv')

test_1 = block.test(sequence_1)

test_2 = block.test(sequence_2)


with open('scores.txt', 'w') as f:
    f.write('Original code, sourpea scores:\n')
    f.write(str(test_1) + '\n')
    f.write('Translated code, sourpea scores:\n')
    f.write(str(test_2) + '\n')