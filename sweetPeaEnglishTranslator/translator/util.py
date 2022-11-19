import os
from fpdf import FPDF

_dirname = os.path.dirname(__file__)
# prompts for code to text
PATH_TO_OUTPUT = os.path.join(_dirname, 'output')


def log(string: str):
    """
    log a string (should be replaced with a more elaborate system
    """
    print(string)


def temp_if_string(string: str, temp_path: str) -> str:
    """
    stores string in file if string is not already a path to a file
    :param string: the string to test and store
    :param temp_path: the path to the temporary file
    :return: path to file
    """
    if not os.path.exists(string):
        log("Creating temporary file")
        f = open(temp_path, 'w')
        f.write(string)
        f.close()
        return temp_path
    return string


def write_to_text(text: str, file_name: str):
    path = os.path.join(PATH_TO_OUTPUT, file_name)
    log(f"Writing translation to file '{path}'...")
    # write translation to file
    with open(path, "w") as f:
        f.write(text)


def write_to_pdf(text: str, file_name: str):
    # write translation to pdf
    # save FPDF() class into a variable pdf
    pdf = FPDF(format='letter', unit='in')

    # Add a page
    pdf.add_page()

    # set style and size of font
    pdf.set_font("Times", size=12)
    effective_page_width = pdf.w - 2 * pdf.l_margin

    # create a cell
    pdf.cell(1.0, 0.0, 'Experiment Design', align='C')
    pdf.ln(0.25)

    # add another cell
    pdf.multi_cell(effective_page_width, 0.25, text, align='L')
    pdf.ln(0.5)

    # save the pdf with name .pdf
    path = os.path.join(PATH_TO_OUTPUT, file_name)
    pdf.output(path)


def write_to_py(text: str, file_name: str):
    path = os.path.join(PATH_TO_OUTPUT, file_name)
    log(f"Writing translation to file '{path}...")
    with open(path, "w") as f:
        f.write(text)


def get_factors(text: str) -> str:
    lines = text.splitlines()
    res = ''
    for line in lines:
        words = line.split()
        if len(words) >= 3:
            if words[2].startswith('Factor') or words[2].startswith('factor'):
                res += line + '\n'
    return res


def get_factors_from_file(path: str) -> str:
    with open(path) as f:
        text = f.read()
    return get_factors(text)


def get_stimuli(text: str) -> str:
    lines = text.splitlines()
    res = ''
    for line in lines:
        words = line.split()
        if len(words) >= 3:
            word = words[2].split('(')
            if word[0].endswith('Stimulus'):
                res += line + '\n'
    return res
