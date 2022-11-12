from sweetPeaEnglishTranslator.translator import pre_process
from sweetPeaEnglishTranslator.translator import translate
import os

_dirname = os.path.dirname(__file__)
PATH_TMP_CHECK_LINE_COMMENTS = os.path.join(_dirname, 'temp/check_line_comments.txt')
PATH_TMP_UNCOMMENT_TEXT = os.path.join(_dirname, 'temp/uncomment_text.txt')
PATH_TMP_CODE_TO_TEXT = os.path.join(_dirname, 'temp/code_to_text.py')
PATH_TMP_TEXT_TO_CODE = os.path.join(_dirname, 'temp/text_to_code.py')


def text_to_code(text, out_path, store_file) -> str:
    _res = translate.text_to_formatted(text)
    return translate.text_to_code(_res, py_file_name=out_path, store_sequence_path=store_file)


def code_to_text(text) -> str:
    return translate.code_to_text(text)


def check_line_comments(text) -> bool:
    return pre_process.check_for_line_comments(text)


def uncomment_text(text) -> str:
    return pre_process.preprocess_text(text)


def comment_text(text) -> str:
    return translate.text_to_formatted(text)


if __name__ == '__main__':
    # to_translate = "test\code_1.py"
    # to_translate = "test/text_4.txt"
    with open("test/code_1.py") as f:
        to_translate = f.read()
    # pre_process.preprocess_text(to_translate, "test/text_1_unformatted.txt")
    # code_f = translate.code_to_formatted(to_translate, export_py=True)
    # print(code_f)
    # translation = "Translation: " + code_to_text(to_translate, export_pdf=True)
    #text_formatted = translate.text_to_formatted(to_translate)
    #code = translate.text_to_code(text_formatted, py_file_name='unformatted_1.py')
    text = translate.code_to_text(to_translate, 'code_1_text.txt')


    # print(text_formatted)
    # code = text_to_code(text_formatted, export_py=True)
    # print(code)
