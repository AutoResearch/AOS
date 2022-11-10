from translate import code_to_text, text_to_code


if __name__ == '__main__':

    #to_translate = "test\code_1.py"
    #translation = "Translation: " + code_to_text(to_translate, export_pdf=True)
    to_translate = "test/text_1.txt"
    code = "Code: " + text_to_code(to_translate, export_py=True)
    print(code)
