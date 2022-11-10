import store_prompts
import extract
from gpt3 import gpt3
import os
import inflect
from fpdf import FPDF

_dirname = os.path.dirname(__file__)
PATH_TO_REGULAR_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors.txt')
PATH_TO_DERIVED_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_derived_factors.txt')
PATH_TO_COUNTERBALANCING_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_counterbalancing.txt')

TRANSITION_STRINGS = ("Transition(", "transition(")
WITHIN_TRIAL_STRINGS = ("WithinTrial(", "within_trial(")
WINDOW_STRINGS = ("Window(", "window(")
NON_CHARACTERS = (" ", ",", "(", ")", "[", "]", ":", ";")

DERIVED_LEVEL_STRINGS = ("DerivedLevel", "derived_level")
FACTOR_STRINGS = ("Factor", "factor")


def translate_regular_factors(to_translate: str):
    """
    A function that translates the regular factors code into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the regular factors code
    """
    prompt = store_prompts.store_prompt_regular_factors(to_translate, PATH_TO_REGULAR_PROMPTS)
    answer, prompt = gpt3(prompt,
                          temperature=0,
                          frequency_penalty=1,
                          presence_penalty=1,
                          start_text='',
                          restart_text='',
                          stop_seq=['Code'])
    stripped_answer = answer.replace("\n\n", "")
    return stripped_answer


def translate_derived_factors_summary(to_translate: str):
    """
    A function that translates the derived factors code into English summary, simply
    enumerating all derived factors.

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the summary of derived factors
    """
    answer = ""
    variable_names = list()
    df_code = extract.extract_derived_factor(to_translate)

    # split code into lines
    lines = df_code.split("\n")
    for line in lines:
        if any(ele in line for ele in FACTOR_STRINGS):
            # split line after the factor definition
            for ele in FACTOR_STRINGS:
                if ele in line:
                    found_variable = False
                    line = line.split(ele)[1]
                    # walk through each character in line and read the variable name
                    read = 0
                    variable_name = ""
                    for character in line:

                        if (character == "\"" or character == "'") and read == 2:
                            variable_names.append(variable_name)
                            break

                        if read == 2:
                            variable_name += character

                        if character == "(":
                            read = 1
                        if (character == "\"" or character == "'") and read == 1:
                            read = 2

    if len(variable_names) == 1:
        answer = "There is another derived factor referred to as " + variable_names[0] + "."
    else:
        if len(variable_names) < 20:
            p = inflect.engine()
            num_variables = p.number_to_words(len(variable_names))
        else:
            num_variables = str(len(variable_names))
        # answer = "There are " + num_variables + " derived factors referred to as " + ", ".join(variable_names) + "."
        answer = "There are " + num_variables + " derived factors: "
        for idx, variable in enumerate(variable_names):
            if idx == len(variable_names) - 1 and len(variable_names) > 2:
                answer += "and " + variable + "."
            elif idx == len(variable_names) - 1 and len(variable_names) == 2:
                answer += "and " + variable + "."
            elif idx == len(variable_names) - 1 and len(variable_names) == 2:
                answer += variable + "."
            elif idx == 0 and len(variable_names) == 2:
                answer += variable
            else:
                answer += variable + ", "

    return answer


def translate_derived_factors(to_translate: str):
    """
    A function that translates the derived factors code into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the derived factors code
    """
    code = extract.extract_derived_factor(to_translate)
    num_derived_factors = extract.get_num_derived_factors(code)
    full_answer = ""

    for i in range(num_derived_factors):
        prompt = store_prompts.store_prompt_derived_factors(to_translate, PATH_TO_DERIVED_PROMPTS, i)
        answer, prompt = gpt3(prompt,
                              temperature=0,
                              frequency_penalty=1,
                              presence_penalty=1,
                              start_text='',
                              restart_text='',
                              stop_seq=['Code'])
        stripped_answer = answer.replace("\n\n", "")
        stripped_answer = stripped_answer.replace("\n", "")
        full_answer += " " + stripped_answer

    return full_answer


def translate_counterbalancing(to_translate: str):
    """
    A function that translates the counterbalancing scheme into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the counterbalancing scheme
    """
    prompt = store_prompts.store_prompt_regular_factors(to_translate, PATH_TO_COUNTERBALANCING_PROMPTS)
    answer, prompt = gpt3(prompt,
                          temperature=0,
                          frequency_penalty=1,
                          presence_penalty=1,
                          start_text='',
                          restart_text='',
                          stop_seq=['Code'])
    stripped_answer = answer.replace("\n\n", "")
    return stripped_answer


def translate_sweetpea_code(to_translate: str, export_txt: bool = False, export_pdf: bool = False):
    """
    A function that translates the sweetpea code into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the sweetpea code
    """
    # create a temporary file if to_translate is not a path
    if not os.path.exists(to_translate):
        print('Creating a temporary file')
        f = open('code_file_temp.py', 'w')
        f.write(to_translate)
        f.close()
        to_translate = 'code_file_temp.py'

    print("Translating sweetpea code '" + to_translate + "'...")
    print("Translating regular factors...")
    translation = translate_regular_factors(to_translate)
    print("Translating derived factors...")
    translation += " " + translate_derived_factors_summary(to_translate)
    translation += " " + translate_derived_factors(to_translate)
    print("Translating counterbalancing scheme...")
    translation += " " + translate_counterbalancing(to_translate)

    # clean up the temp file
    if os.path.exists("code_file_temp.py"):
        os.remove("code_file_temp.py")

    print("Formatting translation...")
    # remove all line breaks from translation
    translation = translation.replace("\n", "")

    # remove double spaces from translation
    translation = translation.replace("  ", " ")

    if export_txt:
        # remove file suffix from string
        output_file = to_translate.split(".")[0] + '.english'

        print("Writing translation to file '" + output_file + "'...")
        # write translation to file
        with open(output_file, "w") as f:
            f.write(translation)

    if export_pdf:
        # remove file suffix from string
        output_file = to_translate.split(".")[0] + '.pdf'

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
        pdf.multi_cell(effective_page_width, 0.25, translation, align='L')
        pdf.ln(0.5)

        # save the pdf with name .pdf
        pdf.output(output_file)

    print("Translation complete.")
    return translation