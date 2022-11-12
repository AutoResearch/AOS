from sweetPeaEnglishTranslator.translator import extract


def store_prompt_simple(to_translate: str, prompt_filename: str, instruction: str) -> str:
    """
    Stores a simple prompt (transformed to lower case) into a string
    :param to_translate: The string to be processed
    :param prompt_filename: The Path to the training set
    :param instruction: The instruction to put at the end
    :return: A string with the prompt
    """
    with open(prompt_filename, 'r') as file:
        stored_string = file.read()
    stored_string += f'\n{to_translate}\n{instruction}'
    return stored_string


def store_prompt_lower_simple(to_translate: str, prompt_filename: str, instruction: str) -> str:
    """
    Stores a simple prompt (transformed to lower case) into a string
    :param sp_filename: The Path to the file with the prompt
    :param prompt_filename: The Path to the training set
    :param instruction: The instruction to put at the end
    :return: A string with the prompt
    """
    with open(prompt_filename, 'r') as file:
        stored_string = file.read()
    stored_string += f'\n{to_translate.lower()}\n{instruction}'
    return stored_string


def store_prompt_regular_factors_code(to_translate: str, prompt_filename: str) -> str:
    """
    A function that stores the GPT-3 prompt and regular factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
    """
    with open(prompt_filename) as file:
        stored_string = file.read()
    stored_string += extract.extract_regular_factor(to_translate) + "\nText:\n"
    return stored_string


def store_prompt_regular_factors_text(to_translate: str, prompt_filename: str) -> str:
    """
    Stores the GPT-3 prompt and the regular factors into a single string
    :param sp_filename: Path to the file containing the text
    :param prompt_filename: Path to the file containing the GPT-3 prompt
    :return: String with prompt and regular factors
    """
    with open(prompt_filename) as file:
        stored_string = file.read()
    stored_string += extract.extract_regular_factor(to_translate) + "\nCode:\n"
    return stored_string


def store_prompt_balancing(to_translate: str, prompt_filename: str) -> str:
    """
    A function that stores the GPT-3 prompt and the code into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
    """
    with open(prompt_filename) as file:
        stored_string = file.read()
    stored_string += extract.extract_main(to_translate) + "\nText:\n"
    return stored_string


def store_prompt_balancing_text(to_translate: str, factors: str, prompt_filename: str) -> str:
    """
    A function that stores the GPT-3 prompt and the code into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
    """
    with open(prompt_filename) as file:
        stored_string = file.read()
    stored_string += factors
    stored_string += extract.extract_main_text(to_translate) + "\nCode:\n"

    return stored_string


def store_prompt_derived_factors(to_translate: str, prompt_filename: str, factor_id: int) -> str:
    """
    A function that stores the GPT-3 prompt and derived factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
        factor_id: the id of the derived factor to be translated
    """
    # first read in the primer prompt for derived factors
    with open(prompt_filename) as file:
        primer = file.read()

    # now read in the full SweetPea code
    full_code = to_translate

    # finally read in the code for all derived factors
    df_code_all = extract.extract_derived_factor(to_translate)

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
    derived_level_expressions = extract.get_derived_levels_from_str(df_code)
    for expression in derived_level_expressions:
        relevant_variable_names.extend(extract.get_variables_from_derived_level_expression(expression))

    # remove duplicates from list
    relevant_variable_names = list(set(relevant_variable_names))

    # now we need to extract the code for the remaining variable names
    helper_code = ""
    for variable in relevant_variable_names:
        helper_code += extract.get_variable_definition(variable, full_code, df_code)

    prompt = primer + helper_code + df_code + "\nText:\n"
    return prompt


def store_prompt_derived_factors_text(to_translate: str, prompt_filename: str, factor_id: int) -> str:
    """
    A function that stores the GPT-3 prompt and derived factors into a
    single string

    Arguments:
        sp_filename: the name of the file containing the SweetPea code
        prompt_filename: the name of the file containing the GPT-3 prompt
        factor_id: the id of the derived factor to be translated
    """
    # first read in the primer prompt for derived factors
    with open(prompt_filename) as file:
        primer = file.read()

    # now read in the full SweetPea code
    full_code = to_translate

    # finally read in the code for all derived factors
    df_code_all = extract.extract_derived_factor(to_translate)

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
    derived_level_expressions = extract.get_derived_levels_from_str(df_code)
    for expression in derived_level_expressions:
        relevant_variable_names.extend(extract.get_variables_from_derived_level_expression(expression))

    # remove duplicates from list
    relevant_variable_names = list(set(relevant_variable_names))

    # now we need to extract the code for the remaining variable names
    helper_code = ""
    for variable in relevant_variable_names:
        helper_code += extract.get_variable_definition(variable, full_code, df_code)

    prompt = primer + helper_code + df_code + "\nCode:\n"
    return prompt
