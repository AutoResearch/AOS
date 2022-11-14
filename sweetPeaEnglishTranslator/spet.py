from sweetPeaEnglishTranslator.translator import pre_process
from sweetPeaEnglishTranslator.translator import translate
from sweetPeaEnglishTranslator.translator import validate
import os

_dirname = os.path.dirname(__file__)
PATH_TMP_CHECK_LINE_COMMENTS = os.path.join(_dirname, 'temp/check_line_comments.txt')
PATH_TMP_UNCOMMENT_TEXT = os.path.join(_dirname, 'temp/uncomment_text.txt')
PATH_TMP_CODE_TO_TEXT = os.path.join(_dirname, 'temp/code_to_text.py')
PATH_TMP_TEXT_TO_CODE = os.path.join(_dirname, 'temp/text_to_code.py')


def text_to_code(text, out_path, store_file) -> str:
    _res = translate.text_to_formatted(text)
    return translate.text_to_code(_res, py_file_name=out_path, store_sequence_path=store_file)


def code_to_text(code, out_path) -> str:
    _res = translate.code_to_formatted(code)
    return translate.code_to_text(_res, pdf_file_name=out_path)


def check_line_comments(text) -> bool:
    return pre_process.check_for_line_comments(text)


def uncomment_text(text) -> str:
    return pre_process.preprocess_text(text)


def uncomment_code(code) -> str:
    return pre_process.preprocess_code(code)


def comment_text(text) -> str:
    return translate.text_to_formatted(text)


def comment_code(code) -> str:
    return translate.code_to_formatted(code)


def text_to_text(text) -> str:
    return validate.text_to_text(text)


def code_to_code(code) -> str:
    return validate.code_to_code(code)


if __name__ == '__main__':
    # to_translate = "test\code_1.py"
    # to_translate = "test/text_4.txt"
    with open("test/text_5.txt") as f:
        to_translate = f.read()
    # pre_process.preprocess_text(to_translate, "test/text_1_unformatted.txt")
    # code_f = translate.code_to_formatted(to_translate, export_py=True)
    # print(code_f)
    # translation = "Translation: " + code_to_text(to_translate, export_pdf=True)
    # text_formatted = translate.text_to_formatted(to_translate)
    # code = translate.text_to_code(text_formatted, py_file_name='unformatted_1.py')
    out = translate.text_to_formatted(to_translate, 'text_5_formatted.txt')

    # print(text_formatted)
    # code = text_to_code(text_formatted, export_py=True)
    # print(code)
