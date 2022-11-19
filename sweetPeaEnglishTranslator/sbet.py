from sweetPeaEnglishTranslator.translator import translate


def check_line_comments(text: str) -> str:
    return True


def uncomment_text(text: str) -> str:
    return text

def uncomment_code(code: str) -> str:
    return code

def comment_text(text: str) -> str:
    res = translate.translate_text_to_formatted_sbet(text)
    return res

def comment_code(code: str) -> str:
    return code

def code_to_text(code: str) -> str:
    return ''


def text_to_code(text, out_path, store_file=None) -> str:
    _text = translate.translate_text_to_formatted_sbet(text)
    res = 'from sweetbean import *\n'
    res += 'from sweetbean.primitives import *\n'
    res += translate.text_to_code_sbet(_text, py_file_name=out_path, prompt_file_name=store_file)
    return res


if __name__ == '__main__':
    with open('test/to_experiment/text_np_full_1.txt') as f:
        _in = f.read()
    _ = translate.translate_text_to_formatted_sbet(_in)
    res = text_to_code(_, 'sbet/py_tmp.py')
    print(res)
