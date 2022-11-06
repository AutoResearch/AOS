import random
import re
import string
from quote import quote

WHITESPACE_LIST = [' ', '(', ')', '[', ']', ',', '=', '+', '-', '{', '}']
QUOTATION_MARKS = ["'", '"']
BLACKLIST = ['factor', 'Factor']
WHITESPACE_CHANCE = .4
REMOVE_WHITESPACE_CHANCE = .2
LINE_COMMENT_CHANCE = .3
INLINE_COMMENT_CHANCE = .005


def scrambling_regular_factor(code_segment, prompt_segment):
    """
    Takes in a code_segment of a regular factor and makes it more randomized (e.g adds white space, comments...)
    Returns a scrambled code thats still valid but 'noisy'
    :param code_segment:
    :return:
    """

    if random.random() < REMOVE_WHITESPACE_CHANCE:
        scrambled_code = _delete_whitespace(code_segment)
    else:
        scrambled_code = _add_whitespace(code_segment)

    scrambled_code, scrambled_prompt = _replace_all(scrambled_code, prompt_segment)
    scrambled_code = _replace_variable_names(scrambled_code)

    scrambled_code = _add_coments(scrambled_code)

    return scrambled_code, scrambled_prompt


def _replace_variable_names(code_segment):
    regex = '[a-z_]+(?=(?:(?:[^\"\n]*\"){2})*[^\"\n]*$)'
    c_s = code_segment
    list1 = re.findall(regex, c_s)
    # print(list1)
    for word in list1:
        c_s_ = list(c_s)
        if word not in BLACKLIST:
            word = list(word)
            c_s = ''
            print(len(word))
            new_word = list(random.choice(string.ascii_lowercase) for _ in range(len(word)))
            for i in range(0, len(c_s_)):
                if i < len(c_s_) - len(word) and i > 0:
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


def _add_coments(code_segment):
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
                comment += ' ' + co + "#"
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
            res_2 += comment

    return res_2
