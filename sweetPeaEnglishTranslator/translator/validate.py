from sweetPeaEnglishTranslator.translator import translate
from sweetPeaEnglishTranslator.translator import pre_process
from sweetPeaEnglishTranslator.translator import util


def text_to_text(text, txt_file_name=None, pdf_file_name=None) -> (str, str):
    # uncomment (this will be our ground truth):
    _t = pre_process.preprocess_text(text)
    # comment per gpt-3:
    _t = translate.text_to_formatted(text)
    # to code per gpt-3:
    _c = translate.text_to_code(_t)
    # uncomment:
    _c = pre_process.preprocess_code(_c)
    # comment per gpt-3:
    _c = translate.code_to_formatted(_c)
    # to text per gpt-3:
    out_text = translate.code_to_text(_c)
    # uncomment (this is the output to compare against)
    out_text = pre_process.preprocess_text(out_text)
    if txt_file_name:
        _res = f'IN:\n{text}\n# ****************** #\nOUT:\n{out_text}'
        util.write_to_text(_res, txt_file_name)
    if pdf_file_name:
        _res = f'IN:\n{text}\n\n\nOUT:\n{out_text}'
        util.write_to_pdf(_res)
    return text, out_text


def code_to_code(code, txt_file_name=None, py_file_name=None) -> str:
    # uncomment:
    _c = pre_process.preprocess_code(code)
    # comment per gpt-3
    _c = translate.code_to_formatted(_c)
    # to text per gpt-3
    _t = translate.code_to_text(_c)
    # uncomment:
    _t = pre_process.preprocess_text(_t)
    # comment per gpt-3:
    _t = translate.text_to_formatted(_t)
    # to code per gpt-3:
    out_code = translate.text_to_code(_t)
    if txt_file_name:
        _res = f'IN:\n{code}\n# ****************** #\nOUT:\n{out_code}'
        util.write_to_text(_res, txt_file_name)
    if py_file_name:
        _res = f'IN:\n{code}\n# ****************** #\nOUT:\n{out_code}'
        util.write_to_py(_res, py_file_name)
    return code, out_code
