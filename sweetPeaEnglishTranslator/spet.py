from sweetPeaEnglishTranslator.translator.translate import code_to_text, text_to_code, _temp_if_string
from sweetPeaEnglishTranslator.translator import pre_process
from sweetPeaEnglishTranslator.translator import translate
import os

_dirname = os.path.dirname(__file__)
PATH_TMP_CHECK_LINE_COMMENTS = os.path.join(_dirname, 'temp/check_line_comments.txt')
PATH_TMP_UNCOMMENT_TEXT = os.path.join(_dirname, 'temp/uncomment_text.txt')
PATH_TMP_CODE_TO_TEXT = os.path.join(_dirname, 'temp/code_to_text.py')
PATH_TMP_TEXT_TO_CODE = os.path.join(_dirname, 'temp/text_to_code.py')


def text_to_code(text, out_path, store_file) -> str:
    path = _temp_if_string(text, PATH_TMP_TEXT_TO_CODE)
    _res = translate.text_to_formatted(path)
    res = translate.text_to_code(_res, add_imports=True, export_py=True, out_path=out_path,
                                 store_sequence_path=store_file)
    if os.path.exists(PATH_TMP_TEXT_TO_CODE):
        os.remove(PATH_TMP_TEXT_TO_CODE)
    return res


def code_to_text(text) -> str:
    path = _temp_if_string(text, PATH_TMP_CODE_TO_TEXT)
    res = translate.code_to_text(path)
    if os.path.exists(PATH_TMP_CODE_TO_TEXT):
        os.remove(PATH_TMP_CODE_TO_TEXT)
    return res


def check_line_comments(text) -> bool:
    path = _temp_if_string(text, PATH_TMP_CHECK_LINE_COMMENTS)
    res = pre_process.check_for_line_comments(path)
    if os.path.exists(PATH_TMP_CHECK_LINE_COMMENTS):
        os.remove(PATH_TMP_CHECK_LINE_COMMENTS)
    return res


def uncomment_text(text) -> str:
    path = _temp_if_string(text, PATH_TMP_UNCOMMENT_TEXT)
    res = pre_process.preprocess_text(path)
    if os.path.exists(PATH_TMP_UNCOMMENT_TEXT):
        os.remove(PATH_TMP_UNCOMMENT_TEXT)
    return res


def comment_text(text) -> str:
    return translate.text_to_formatted(text)


if __name__ == '__main__':
    # to_translate = "test\code_1.py"
    # to_translate = "test/text_4.txt"
    to_translate = "test/text_unformatted_1.txt"
    # pre_process.preprocess_text(to_translate, "test/text_1_unformatted.txt")
    # code_f = translate.code_to_formatted(to_translate, export_py=True)
    # print(code_f)
    # translation = "Translation: " + code_to_text(to_translate, export_pdf=True)
    text_formatted = translate.text_to_formatted(to_translate)
    code = translate.text_to_code(text_formatted, export_py=True)

    # print(text_formatted)
    # code = text_to_code(text_formatted, export_py=True)
    # print(code)
