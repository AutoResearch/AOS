from sweetPeaEnglishTranslator.translator import translate


def text_to_code(text, out_path, store_file) -> str:
    res = translate.text_to_code_sbet(text, py_file_name=out_path, prompt_file_name=store_file)
    _translation = 'from sweetbean.primitives import *\n'
    res = _translation + res
    return res


if __name__ == '__main__':
    with open('test/to_experiment/text_np_full_1.txt') as f:
        text = f.read()
    _ = translate.translate_text_to_formatted_sbet(text)
    res = text_to_code(_, 'sbet/py_tmp.py', 'sbet/prompt.txt')
    #print(res)
