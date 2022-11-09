from gpt3 import gpt3
import sys
import os
from time import sleep
import warnings
import inflect
from fpdf import FPDF
import os

REGULAR_FACTORS = "### REGULAR FACTORS"
DERIVED_FACTORS = "### DERIVED FACTORS"
BALANCING = "### EXPERIMENT"
END_OF_SWEETPEA_CODE = "### END OF EXPERIMENT DESIGN"

TRANSITION_STRINGS = ("Transition(", "transition(")
WITHIN_TRIAL_STRINGS = ("WithinTrial(", "within_trial(")
WINDOW_STRINGS = ("Window(", "window(")
NON_CHARACTERS = (" ", ",", "(", ")", "[", "]", ":", ";")

DERIVED_LEVEL_STRINGS = ("DerivedLevel", "derived_level")
FACTOR_STRINGS = ("Factor", "factor")

_dirname = os.path.dirname(__file__)
PATH_TO_REGULAR_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors.txt')
PATH_TO_DERIVED_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_derived_factors.txt')
PATH_TO_COUNTERBALANCING_PROMPTS = os.path.join(_dirname, 'prompts/gpt3prompt_counterbalancing.txt')

def extract_code_segment(filename: str, reg_fac_line: str) -> str:
    """
    A function that extracts SweetPea code for the definition of regular factors from
    a file

    Arguments:
        filename: the name of the file containing the SweetPea code
        reg_fac_line: the keyword used to identify a section of the code

    Returns:
        A string containing the SweetPea code for a given section
    """
    extracted_code = ""
    file = open(filename)
    line = file.readline().strip()  # initially holds first line of file
    while line != reg_fac_line:
        line = file.readline().strip()  # next line
    if line == reg_fac_line:
        line = file.readline().strip()
        while "###" not in line:  # stops when next # is found
            extracted_code += line + "\n"
            line = file.readline().strip()
    file.close()
    return extracted_code


def extract_rf(filename: str) -> str:
    """
    A function that extracts the regular factors code from a SweetPea code file

    Arguments:
        filename: the name of the file containing the SweetPea code

    Returns:
        A string containing the regular factors code
    """
    return extract_code_segment(filename, REGULAR_FACTORS)


def extract_df(filename: str) -> str:
    """
    A function that extracts the derived factors code from a SweetPea code file

    Arguments:
        filename: the name of the file containing the SweetPea code

    Returns:
        A string containing the derived factors code
    """

    return extract_code_segment(filename, DERIVED_FACTORS)


def extract_main_code(filename: str) -> str:
    """
    A function that extracts the regular factors code from a SweetPea code file

    Arguments:
        filename: the name of the file containing the SweetPea code

    Returns:
        A string containing the regular factors code
    """
    extracted_code = ""
    file = open(filename)
    line = file.readline()

    # reads in only relevant parts of the code
    while line:
        if line.strip() == REGULAR_FACTORS or line.strip() == DERIVED_FACTORS or line.strip() == BALANCING:
            line = file.readline()
            while line.strip() != REGULAR_FACTORS \
                    and line.strip() != DERIVED_FACTORS \
                    and line.strip() != BALANCING \
                    and line.strip() != END_OF_SWEETPEA_CODE:  # stops when next code section is found
                extracted_code += line.strip() + "\n"
                line = file.readline()

        if line.strip == END_OF_SWEETPEA_CODE:
            break

        if line.strip() != REGULAR_FACTORS and line.strip() != DERIVED_FACTORS and line.strip() != BALANCING:
            line = file.readline()

    # convert code to lines
    extracted_code = extracted_code.split("\n")
    for line in extracted_code:
        if len(line) > 0:
            if line[0] == "#":
                extracted_code.remove(line)

    extracted_code = "\n".join(extracted_code)
    extracted_code = extracted_code.replace("\n\n", "\n")

    return extracted_code


def store_prompt_rf(sp_filename: str, prompt_filename: str) -> str:
    """
    A function that stores the GPT-3 prompt and regular factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
    """
    stored_string = ""
    with open(prompt_filename) as file:
        for line in file:
            stored_string += line
    stored_string += extract_rf(sp_filename) + "\nText:\n"

    return stored_string


def store_prompt_balancing(sp_filename: str, prompt_filename: str) -> str:
    """
    A function that stores the GPT-3 prompt and regular factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
    """
    stored_string = ""
    with open(prompt_filename) as file:
        for line in file:
            stored_string += line
    stored_string += extract_main_code(sp_filename) + "\nText:\n"

    return stored_string


def store_prompt_df(sp_filename: str, prompt_filename: str, factor_id: int) -> str:
    """
    A function that stores the GPT-3 prompt and derived factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
        factor_id: the id of the derived factor to be translated
    """
    # first read in the primer prompt for derived factors
    primer = ""
    with open(prompt_filename) as file:
        for line in file:
            primer += line

    # now read in the full SweetPea code
    full_code = ""
    with open(sp_filename) as file:
        for line in file:
            full_code += line

    # finally read in the code for all derived factors
    df_code_all = extract_df(sp_filename)

    # break code into list of strings by line break
    code_list = df_code_all.split("\n")
    df_code = ""

    # extract the code for the derived factor with the given id
    id = -1
    read = False
    for line in code_list:
        if "##" in line:
            id += 1

        if read:
            if factor_id == id:
                df_code += line + "\n"
            else:
                break

        if factor_id == id:
            read = True

    # now we need to parse the code for the derived factor to identify other
    # derived factors that are relevant to the translation for this derived factor
    relevant_variable_names = list()
    derived_level_expressions = get_derived_levels_from_str(df_code)
    for expression in derived_level_expressions:
        relevant_variable_names.extend(get_variables_from_derived_level_expression(expression))

    # remove duplicates from list
    relevant_variable_names = list(set(relevant_variable_names))

    # now we need to extract the code for the remaining variable names
    helper_code = ""
    for variable in relevant_variable_names:
        helper_code += get_variable_definition(variable, full_code, df_code)

    prompt = primer + helper_code + df_code + "\nText:\n"
    return prompt


def get_variable_definition(variable: list, full_code: list, sub_code=""):
    """
    A function that returns the definition of a variable from the SweetPea code

    Arguments:
        variable: the variable to be checked
        full_code: the full SweetPea code as a list of strings
        sub_code: if the variable is defined in the sub code then it is not searched for in the full code
        as a list of strings

    Returns:
        The definition of the variable as a string
    """
    variable_definition = ""
    # first we need to check if the variable isn't already defined in the sub code

    # divide subcode into list of strings by line break
    sub_code_list = sub_code.split("\n")
    for line in sub_code_list:
        if line.startswith(variable + " ") or line.startswith(variable + "="):
            return variable_definition

    # if the variables is not defined in the sub code then search in the full code

    # concatenate two lists
    VALID_DEFINITIONS = DERIVED_LEVEL_STRINGS + FACTOR_STRINGS

    # divide full code into list of strings by line break
    relevant_line_number = -1
    full_code_list = full_code.split("\n")
    for idx, line in enumerate(full_code_list):
        if line.startswith(variable + " ") or line.startswith(variable + "="):
            if any(ele in line for ele in VALID_DEFINITIONS):
                relevant_line_number = idx
                break

    if relevant_line_number == -1:
        warnings.warn(
            "Warning: I was looking for variable " + variable + ". But it is not defined in the SweetPea code")
        return variable_definition

    # extract the relevant line from the full code
    parentheses_count = 0
    relevant_lines = list()

    for idx, line in enumerate(full_code_list):
        if idx >= relevant_line_number:
            relevant_lines.append(line)
            for char in line:
                if char == "(":
                    parentheses_count += 1
                elif char == ")":
                    parentheses_count -= 1
            if parentheses_count == 0:
                break

    # concatenate the relevant lines
    for line in relevant_lines:
        variable_definition += line + "\n"

    return variable_definition


def get_variables_from_derived_level_expression(expression: str):
    """
    A function that returns a list of variables that occur in the definition of a derived level

    Arguments:
        expression: the expression to be checked

    Returns:
        A list of variables in the given expression
    """
    variables = list()

    # extract variables for transition factor
    for transition_string in TRANSITION_STRINGS:
        if transition_string in expression:
            # extract the variable name
            remaining_line = expression.split(transition_string)[-1]
            # cut string until first occurrence of ","
            remaining_line = remaining_line.split(",")[1:]
            # convert list back to string
            remaining_line = "".join(remaining_line)
            variables.extend(read_variable_from_expression(remaining_line))

    # extract variables for within trial factor
    for within_trial_string in WITHIN_TRIAL_STRINGS:
        if within_trial_string in expression:
            # extract the variable name
            remaining_line = expression.split(within_trial_string)[-1]
            # cut string until first occurrence of ","
            remaining_line = remaining_line.split(",")[1:]
            # convert list back to string
            remaining_line = "".join(remaining_line)
            variables.extend(read_variable_from_expression(remaining_line))

    # extract variables for window factor
    for window_string in WINDOW_STRINGS:
        if window_string in expression:
            # extract the variable name
            remaining_line = expression.split(window_string)[-1]
            # cut string until first occurrence of ","
            remaining_line = remaining_line.split(",")[1:]
            # convert list back to string
            remaining_line = "".join(remaining_line)
            variables.extend(read_variable_from_expression(remaining_line))

    return variables


def read_variable_from_expression(expression: str):
    """
    A function that returns a list of variable name from any single-line expression

    Arguments:
        expression: the expression to be checked

    Returns:
        The list of variables from the given expression
    """
    variables = list()

    variable = ""
    for char in expression:
        if char not in NON_CHARACTERS:
            variable += char
        else:
            if variable != "":
                variables.append(variable)
                variable = ""

    return variables


def get_derived_levels_from_str(code: str) -> list:
    """
    A function that returns a list of the expressions for levels of the derived factors in the
    given code

    Arguments:
        code: the code to be checked

    Returns:
        A list of expressions for levels of the derived factors in the given code
    """
    level_expressions = list()

    # search for all occurrences of the text "DerivedLevel" in the code
    derived_levels = code.split("\n")

    for line in derived_levels:
        for derived_level_string in DERIVED_LEVEL_STRINGS:
            if derived_level_string in line:
                level_expressions.append(line)

    return level_expressions


def get_num_derived_factors(text: str):
    """
    A function that returns the number of derived factors in the text

    Arguments:
        text: the text to be checked

    Returns:
        The number of derived factors in the text
    """

    # count number of occurrences "##" in text
    num_derived_factors = text.count("##")

    return num_derived_factors


def translate_regular_factors(to_translate: str):
    """
    A function that translates the regular factors code into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the regular factors code
    """
    prompt = store_prompt_rf(to_translate, PATH_TO_REGULAR_PROMPTS)
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
    df_code = extract_df(to_translate)

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
    code = extract_df(to_translate)
    num_derived_factors = get_num_derived_factors(code)
    prompt = store_prompt_rf(to_translate, PATH_TO_DERIVED_PROMPTS)
    full_answer = ""

    for i in range(num_derived_factors):
        prompt = store_prompt_df(to_translate, prompt, i)
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
    prompt = store_prompt_rf(to_translate, PATH_TO_COUNTERBALANCING_PROMPTS)
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


def display_typed_text(text: str):
    """
    A function that displays the text as if it was typed

    Arguments:
        text: the text to be displayed
    """
    for char in text:
        sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()


if __name__ == '__main__':
    # to_translate = "unextracted_code.py"
    # translation = "Translation: " + translate_regular_factors(to_translate)
    # translation = "Translation: " + translate_derived_factors_summary(to_translate)
    # translation = "Translation: " + translate_derived_factors(to_translate)
    # translation = "Translation: " + translate_counterbalancing(to_translate)
    # display_typed_text(translation)
    test_string = '### REGULAR FACTORS\n' \
                  'object = Factor("object identity", [Level("H", 2), Level("S", 1)])\n' \
                  'motion = Factor("motion", [Level("left", 2), Level("right", 3)])\n' \
                  '### DERIVED FACTORS\n' \
                  'def response_left(object):\n' \
                  '    return object == "H"\n' \
                  'def response_right(object):\n' \
                  '    return object == "S"\n' \
                  'response = Factor("correct response", [' \
                  'DerivedLevel("left", WithinTrial(response_left, [object])),' \
                  'DerivedLevel("right", WithinTrial(response_right, [object])),])\n' \
                  '### EXPERIMENT\n' \
                  'constraints = [at_most_k_in_a_row(5, response),' \
                  'minimum_trials(100)]\n' \
                  'design = [object, motion, response]\n' \
                  'crossing = [object, motion,]\n' \
                  'block = fully_cross_block(design, crossing, constraints)\n' \
                  'experiments = synthesize_trials_non_uniform(block, 1)\n' \
                  '### END OF EXPERIMENT DESIGN\n' \
                  'print_experiments(block, experiments)'

    to_translate = "test\code_1.py"
    translation = "Translation: " + translate_sweetpea_code(test_string, export_pdf=True)
    print(translation)
