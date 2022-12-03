from sweetPeaEnglishTranslator.translator import translate, pre_process, util
from sweetPeaEnglishTranslator import gpt3
import time
import random

ALTER_TEXT_INSTRUCTIONS = [('Rephrase this as a scientist', .5), ('Paraphrase as a scientific text', .5)]

SLEEP_TIME = 30

def sweetToSour(infile):
    with open(infile) as f:
        sweet = f.read()
    sweet_lines = sweet.splitlines()
    res = ''
    for line in sweet_lines:
        if line.startswith('import') or line.startswith('from'):
            pass
        else:
            res += line + '\n'
    res = 'from sourpea import *\nfrom sourpea.primitives import *\nfrom sourpea.util import *' + res
    with open(infile[:-3] + '_sour.py', 'w') as f:
        f.write(res)


def codeToCode(infile, alterText=False):
    with open(infile) as f:
        code_1 = f.read()
    _code_preprocessed = pre_process.preprocess_code(code_1)
    code_1_formatted = translate.code_to_formatted(_code_preprocessed)
    time.sleep(SLEEP_TIME)
    with open(infile[:-3] + '_formatted_tmp.py', 'w') as f:
        f.write(code_1_formatted)
    text_1 = translate.code_to_text(code_1_formatted)
    time.sleep(SLEEP_TIME)
    with open(infile[:-9] + 'text_1.txt', 'w') as f:
        f.write(text_1)
    if alterText:
        instruction = random.choice(ALTER_TEXT_INSTRUCTIONS)
        print(f'Altering text with instructions: {instruction[0]}')
        text_1 = gpt3.gpt3_edit(text_1, instruction[0], temperature=instruction[1])
        time.sleep(SLEEP_TIME)
        with open(infile[:-9] + 'text_1_altered.txt', 'w') as f:
            f.write(text_1)
    _text_1_preprocessed = pre_process.preprocess_text(text_1)
    txt_formatted = translate.text_to_formatted(_text_1_preprocessed)
    time.sleep(SLEEP_TIME)
    with open(infile[:-9] + 'text_1_formatted_tmp.txt', 'w') as f:
        f.write(txt_formatted)
    _code_2 = translate.text_to_code(txt_formatted)
    time.sleep(SLEEP_TIME)
    code_2 = "from sweetpea import *\n"+ _code_2 + "\nsave_experiments_csv(block, experiments, 'code_2_sequences/seq')"
    with open(infile[:-4] + '2.py', 'w') as f:
        f.write(code_2)
    _code_2_preprocessed = pre_process.preprocess_code(code_2)
    code_2_formatted = translate.code_to_formatted(_code_preprocessed)
    time.sleep(SLEEP_TIME)
    with open(infile[-4] + '2_formatted_tmp.py', 'w') as f:
        f.write(code_2_formatted)
    text_2 = translate.code_to_text(code_2_formatted)
    with open(infile[:-9] + 'text_2.txt', 'w') as f:
        f.write(text_2)



if __name__ == '__main__':
    codeToCode('altered_text/example_2/code_1.py', True)
