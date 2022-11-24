from sweetPeaEnglishTranslator.translator import translate, pre_process, util
import time


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


def codeToCode(infile):
    with open(infile) as f:
        code_1 = f.read()
    _ = pre_process.preprocess_code(code_1)
    formatted = translate.code_to_formatted(_)
    time.sleep(15)
    with open(infile[:-3] + '_formatted_gpt3.py', 'w') as f:
        f.write(formatted)
    txt = translate.code_to_text(formatted)
    time.sleep(15)
    with open(infile[:-3] + '_text_gpt3.txt', 'w') as f:
        f.write(txt)
    _t = pre_process.preprocess_text(txt)
    txt_formatted = translate.text_to_formatted(_t)
    time.sleep(15)
    with open(infile[:-3] + '_text_formatted_gpt3.txt', 'w') as f:
        f.write(txt_formatted)
    code_2 = translate.text_to_code(txt_formatted)
    code_2 = "from sweetpea import *\nfrom sweetpea.primitives import *\n" + code_2 + "save_experiments_csv(block, experiments, 'code_2_sequences/seq')"
    with open(infile[:-3] + '_code_gpt3.py', 'w') as f:
        f.write(code_2)


if __name__ == '__main__':
    sweetToSour('example_2/code_1.py')
    #codeToCode('example_2/code_1.py')
