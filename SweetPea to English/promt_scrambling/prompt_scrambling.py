import random
import re
import string
from quote import quote

WHITESPACE_LIST = ['(', ')', '[', ']', ',', '=', '+', '-', '{', '}']
QUOTATION_MARKS = ["'", '"']
# TODO: update Blacklist whenever you see something weird!
BLACKLIST = ['factor', 'Factor',
             'Level',
             'derived_level', 'DerivedLevel',
             'def', 'not', 'return', 'or', 'and',
             'within_trial', 'WithinTrial',
             'transition', 'Transition',
             "window",
             "minimum_trials",
             "exclude", "fully_cross_block", "require_complete_crossing",
             "synthesize_trials_non_uniform", "no_more_than_k_in_a_row", "simple_level", "FullyCross",
             "MultipleCross", "Derivation", "at_most_k_in_a_row", "AtMostKInARow", "at_least_k_in_a_row",
             "AtLeastKInARow", "exactly_k", "ExactlyK", "exactly_k_in_a_row", "ExactlyKInARow", "exclude", "Exclude",
             "MultipleCrossBlock", "Block", "FullyCrossBlock",
             "AtMostKInARow", "CrossBlock", "synthesize_trials", "print_experiments",
             "CMSGen", "IterateGen", "RandomGen", "MinimumTrials", 'Level', 'SimpleLevel', 'DerivedLevel', 'ElseLevel',
             'Factor', 'SimpleFactor', 'DerivedFactor', 'DerivationWindow', 'WithinTrialDerivationWindow',
             'TransitionDerivationWindow', 'WithinTrial', 'Transition', 'Window', 'simple_level', 'derived_level',
             'else_level', 'factor', 'within_trial', 'transition', 'window', "print_experiments",
             "synthesize_trials_uniform", "synthesize_trials_non_uniform"]
KEYWORD_DICT = [{'factor': 'Factor', 'Factor': 'factor',
                 'derived_level': 'DerivedLevel', 'DerivedLevel': 'derived_level',
                 'within_trial': 'WithinTrial', 'WithinTrial': 'within_trial',
                 'transition': 'Transition', 'Transition': 'transition'}]
WHITESPACE_CHANCE = .4
REMOVE_WHITESPACE_CHANCE = .2
LINE_COMMENT_CHANCE = .3
INLINE_COMMENT_CHANCE = .005
CHANCE_VARIABLE_DECLARATION = .1


def scramble_prompt(code_segment, text_segment):
    """
    Takes in a code_segment of a regular factor and makes it more randomized (e.g adds white space, comments...)
    Returns a scrambled code that's still valid but 'noisy'
    :param code_segment: the code segment to be randomized
    :param text_segment: the text segment to randomized
    :return:
    """

    if random.random() < REMOVE_WHITESPACE_CHANCE:
        scrambled_code = _delete_whitespace(code_segment)
    else:
        scrambled_code = _add_whitespace(code_segment)

    scrambled_code, scrambled_prompt = _replace_all(scrambled_code, text_segment)
    scrambled_code = _replace_variable_names(scrambled_code)

    #scrambled_code = _add_comments(scrambled_code)
    scrambled_code = _replace_variable_declaration(scrambled_code)

    return scrambled_code, scrambled_prompt


def _replace_variable_declaration(code_segment):
    c_s = code_segment
    is_start = True
    starts = []
    ends = []
    for i in range(len(code_segment)):
        c = code_segment[i]
        if c == '"':
            if is_start:
                starts.append(i)
                is_start = False
            else:
                ends.append(i)
                is_start = True
    for s, e in zip(starts, ends):
        if random.random() < CHANCE_VARIABLE_DECLARATION:
            if random.random() < .4:
                c_s = __switch_variable_witch_declare_standard(code_segment, code_segment[s: e + 1])
            elif random.random() < .5:
                c_s = __switch_variable_witch_declare_list(code_segment, code_segment[s: e + 1])
            elif random.random() < .8:
                c_s = __switch_variable_witch_declare_dictonary(code_segment, code_segment[s: e + 1])
    return c_s


def __switch_variable_witch_declare_standard(code_segment, variable):
    declaration = __get_random_word(__get_random_number(3, 10))
    c_s = code_segment.replace(variable, declaration)
    return declaration + "=" + variable + '\n' + c_s


def __switch_variable_witch_declare_list(code_segment, variable):
    declaration = __get_random_word(__get_random_number(3, 10))
    lst = '['
    index = __get_random_number(0, 10)
    c_s = code_segment.replace(variable, declaration + "[" + str(index) + "]")
    for i in range(index):
        lst += '"' + __get_random_word(__get_random_number(2, 6)) + '",'
    lst += variable
    appendix = __get_random_number(0, 10)
    for i in range(appendix):
        lst += ',"' + __get_random_word(__get_random_number(2, 6)) + '"'
    lst += ']'
    c_s = declaration + "=" + lst + '\n' + c_s
    return c_s


def __switch_variable_witch_declare_dictonary(code_segment, variable):
    declaration = __get_random_word(__get_random_number(3, 10))
    dic = '{'
    while random.random() < .7:
        dic += '"' + __get_random_word(__get_random_number(4, 8)) + '":"' + __get_random_word(
            __get_random_number(4, 8)) + '",'
    _key = '"' + __get_random_word(__get_random_number(4, 8)) + '"'
    dic += _key + ':' + variable
    while random.random() < .7:
        dic += ',"' + __get_random_word(__get_random_number(4, 8)) + '":"' + __get_random_word(
            __get_random_number(4, 8)) + '"'
    dic += '}'
    c_s = code_segment.replace(variable, declaration + "[" + _key + "]")
    c_s = declaration + "=" + dic + '\n' + c_s
    return c_s


def _replace_variable_names(code_segment):
    regex = '[a-z_]+(?=(?:(?:[^\"\n]*\"){2})*[^\"\n]*$)'
    c_s = code_segment
    list1 = re.findall(regex, c_s)
    for word in list1:
        c_s_ = list(c_s)
        if word not in BLACKLIST:
            word = list(word)
            c_s = ''
            new_word = list(random.choice(string.ascii_lowercase) for _ in range(len(word)))
            for i in range(0, len(c_s_)):
                if len(c_s_) - len(word) > i > 0:
                    if c_s_[i:i + len(word)] == word:
                        if (len(list(filter(lambda x: x in QUOTATION_MARKS, c_s_[i + len(word):]))) % 2) == 0:
                            c_s_[i:i + len(word)] = new_word
                c_s += c_s_[i]
    return c_s


def _replace_all(code_segment, prompt_segment):
    regex = r'\w+'
    c_s = code_segment
    p_s = prompt_segment
    list1 = re.findall(regex, c_s)
    for word in list1:
        if random.random() < 1 / (len(list1) + 1) and word not in BLACKLIST:
            new_word_length = round(random.random() * 4) + 3
            new_word = ''.join(random.choice(string.ascii_lowercase) for _ in range(new_word_length))
            c_s = c_s.replace(word, new_word)
            p_s = p_s.replace(word, new_word)
    return c_s, p_s


def _delete_whitespace(segment):
    return "".join(filter(lambda x: x != ' ', segment))


def _add_whitespace(segment):
    res = ''
    for c in segment:
        if c == '\n':
            while random.random() < WHITESPACE_CHANCE:
                res += '\n'
        if c in WHITESPACE_LIST:
            while random.random() < WHITESPACE_CHANCE:
                res += ' '
        res += c
        if c in WHITESPACE_LIST:
            while random.random() < WHITESPACE_CHANCE:
                res += ' '
    return res


def _add_comments(code_segment):
    regex = r'\w+'
    c_s = code_segment
    list1 = re.findall(regex, c_s)
    res = ''
    for c in c_s:
        res += c
        if c == ' ' and random.random() < INLINE_COMMENT_CHANCE:
            w = random.choice(list1)
            qu = quote(w, limit=1)
            comment = '#'
            if qu:
                co = qu[0]['quote'].replace('\n', ' ')
                comment += ' ' + co
            comment += ' #'
            res += comment
    res_2 = ''
    for c in res:
        res_2 += c
        if c == '\n' and random.random() < LINE_COMMENT_CHANCE:
            w = random.choice(list1)
            qu = quote(w, limit=1)
            comment = '#'
            if qu:
                co = qu[0]['quote'].replace('\n', ' ')
                comment += ' ' + co
            comment += '\n'
            res_2 += comment

    return res_2


def __get_random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def __get_random_number(min_length, max_length):
    return round(random.random() * (max_length - min_length) + min_length)
