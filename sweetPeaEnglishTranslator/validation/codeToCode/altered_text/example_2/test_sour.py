from sourpea import *
from sourpea.primitives import *
from sourpea.util import *

letter = Factor('letter', ['b', 'f', 'm', 'q', 'k', 'x', 'r', 'h'])

def is_target(letters):
    return letters[0] == letters[2]


def is_not_target(letters):
    return not is_target(letters)


one_t = DerivedLevel(1, DerivationWindow(is_target, [letter], 3), 1)
two_t = DerivedLevel(2, DerivationWindow(is_not_target, [letter], 3), 5)

target = Factor('target', [one_t, two_t])


def is_one_back(letters):
    return letters[0] == letters[1]


def is_not_one_back(letters):
    return not is_one_back(letters)


two_o = DerivedLevel(2, DerivationWindow(is_one_back, [letter], 2), 1)
one_o = DerivedLevel(1, DerivationWindow(is_not_one_back, [letter], 2), 5)

one_back = Factor('one back', [one_o, two_o])


def is_control_target(letters):
    return is_target(letters) and letters[2] != letters[1]


def is_experimental_target(letters):
    return is_target(letters) and letters[2] == letters[1]


def is_control_foil(letters):
    return is_not_target(letters) and letters[2] != letters[1]


def is_experimental_foil(letters):
    return is_not_target(letters) and letters[2] == letters[1]


one_one_0 = DerivedLevel('1/1/0', DerivationWindow(is_control_target, [letter], 3), 3)
one_two_0 = DerivedLevel('1/2/0', DerivationWindow(is_experimental_target, [letter], 3), 1)
two_one_0 = DerivedLevel('2/1/0', DerivationWindow(is_control_foil, [letter], 3), 17)
two_two_0 = DerivedLevel('2/2/0', DerivationWindow(is_experimental_foil, [letter], 3), 3)

condi = Factor('condi', [one_one_0, one_two_0, two_one_0, two_two_0])

block_1 = Block(design=[letter, target, one_back, condi], crossing=[letter, target])
block_2 = Block(design=[letter, target, one_back, condi], crossing=[one_back], constraints=[MinimumTrials(48)])
block_3 = Block(design=[letter, target, one_back, condi], crossing=[condi], constraints=[MinimumTrials(48)])

sequence_1 = trials_from_csv('code_1_sequences/seq_0.csv')
sequence_2 = trials_from_csv('code_2_sequences/seq_0.csv')

test_1 = block_1.test(sequence_1)
test_2 = block_2.test(sequence_1)
test_3 = block_3.test(sequence_1)

test_4 = block_1.test(sequence_2)
test_5 = block_2.test(sequence_2)
test_6 = block_3.test(sequence_2)


with open('scores.txt', 'w') as f:
    f.write('Original code, sourpea scores:\n')
    f.write(str(test_1) + '\n')
    f.write(str(test_2) + '\n')
    f.write(str(test_3) + '\n')
    f.write('Translated code, sourpea scores:\n')
    f.write(str(test_4) + '\n')
    f.write(str(test_5) + '\n')
    f.write(str(test_6) + '\n')