from sweetPeaEnglishTranslator.translator.translate import code_to_text, text_to_code, text_to_formatted

if __name__ == '__main__':
    # to_translate = "test\code_1.py"
    # to_translate = "test/text_4.txt"
    to_translate = "test/text_unformatted_1.txt"

    # translation = "Translation: " + code_to_text(to_translate, export_pdf=True)
    text_formatted = text_to_formatted(to_translate)
    print(text_formatted)
    code = text_to_code(text_formatted, export_py=True)
    print(code)
