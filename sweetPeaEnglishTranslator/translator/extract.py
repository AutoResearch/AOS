import sys
from time import sleep
import warnings
from sweetPeaEnglishTranslator.translator.constants import *


def extract_segment(text: str, reg_fac_line: str) -> str:
    """
    A function that extracts text segments
    Arguments:
        filename: the name of the file containing the SweetPea code
        reg_fac_line: the keyword used to identify a section of the code

    Returns:
        A string containing the SweetPea code for a given section
    """
    extracted_code = ""
    lines = text.splitlines()
    i = 0  # initially holds first line of file
    while i < len(lines) and not lines[i].startswith(reg_fac_line):
        i += 1
    if i < len(lines) and lines[i].startswith(reg_fac_line):
        i += 1
        while i < len(lines) and not lines[i].startswith('###'):  # stops when next # is found
            extracted_code += f'{lines[i]}\n'
            i += 1
    if not extracted_code:
        raise Exception("Error in extract_segment: No segment found")
    return extracted_code


def extract_regular_factor(filename: str) -> str:
    return extract_segment(filename, REGULAR_FACTORS)


def extract_derived_factor(filename: str) -> str:
    return extract_segment(filename, DERIVED_FACTORS)


def extract_main(text: str) -> str:
    """
    A function that extracts the SweetPea code from a SweetPea code file

    Arguments:
        filename: the name of the file containing the SweetPea code

    Returns:
        A string containing the regular factors code
    """
    extracted_code = ""
    lines = text.splitlines()
    i = 0

    # reads in only relevant parts of the code
    while i < len(lines):
        if lines[i].strip() == REGULAR_FACTORS or lines[i].strip() == DERIVED_FACTORS or lines[i].strip() == BALANCING:
            i += 1
            while i < len(lines) \
                    and lines[i].strip() != REGULAR_FACTORS \
                    and lines[i].strip() != DERIVED_FACTORS \
                    and lines[i].strip() != BALANCING \
                    and lines[i].strip() != END_OF_SWEETPEA_CODE:  # stops when next code section is found
                extracted_code += f'{lines[i].strip()}\n'
                i += 1

        if i < len(lines) and lines[i].strip == END_OF_SWEETPEA_CODE:
            break

        if i < len(lines) and lines[i].strip() != REGULAR_FACTORS and lines[i].strip() != DERIVED_FACTORS and lines[
            i].strip() != BALANCING:
            i += 1

    # convert code to lines
    extracted_code = extracted_code.split("\n")
    for line in extracted_code:
        if len(line) > 0:
            if line[0] == "#":
                extracted_code.remove(line)

    extracted_code = "\n".join(extracted_code)
    extracted_code = extracted_code.replace("\n\n", "\n")

    return extracted_code


def extract_main_text(filename: str) -> str:
    """
    Extract the counterbalance part of the text
    :param filename: Path to the file with the text
    :return: A string containing the counterbalance pert
    """
    return extract_segment(filename, BALANCING)


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
