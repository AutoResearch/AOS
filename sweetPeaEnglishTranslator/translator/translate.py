from sweetPeaEnglishTranslator.translator import store_prompts
from sweetPeaEnglishTranslator.translator import extract
from sweetPeaEnglishTranslator.gpt3 import gpt3
import inflect
from sweetPeaEnglishTranslator.translator import post_process
from sweetPeaEnglishTranslator.translator.constants import *
from sweetPeaEnglishTranslator.translator import util



def translate(to_translate: str, path_to_prompt: str, preamble: str = ''):
    """
    Args:
        to_translate:
        path_to_prompt:
        keyword_start:
        keyword_stop:

    Returns:
    """
    if not to_translate:
        return ''
    prompt = store_prompts.store_prompt(to_translate, path_to_prompt, preamble)
    answer, _ = gpt3(prompt, stop_seq=['*Human'])
    return answer


def translate_text_to_formatted_sbet(to_translate: str, preamble: str = ''):
    return translate(to_translate, PATH_FORMAT_TEXT_SBET, preamble) + '### END'


def translate_regular_to_code_sbet(to_translate: str, preamble: str = ''):
    _ = extract.extract_segment(to_translate, REGULAR_STIMULI_SPET)
    return translate(_, PATH_REGULAR_TEXT_SBET, preamble)


def translate_conditional_to_code_sbet(to_translate: str, preamble: str = ''):
    _ = extract.extract_segment(to_translate, CONDITIONAL_STIMULI_SPET)
    _lst = extract.extract_all_segments_as_list(_)
    res = ''
    for i in _lst:
        res += translate(i, PATH_CONDITIONAL_TEXT_SBET, preamble)
    return res


def translate_trial_block_to_code_sbet(to_translate: str, preamble: str = ''):
    _ = extract.extract_segment(to_translate, TRIAL_BLOCK_SPET)
    return translate(_, PATH_TRIAL_BLOCK_TEXT_SBET, preamble)


def translate_text_to_formatted(to_translate: str) -> str:
    """
    Add hashtags and reorganize text
    :param to_translate: The text to be translated
    :return: A string containing the formated text
    """
    prompt = store_prompts.store_prompt_lower_simple(to_translate, PATH_TO_FORMAT_TEXT, 'Formatted:')
    answer, prompt = gpt3(prompt, response_length=1024, stop_seq=['Unformatted:'])
    return answer


def translate_code_to_formatted(to_translate: str) -> str:
    """
    Add hashtags and reorganize code
    :param to_translate: The code to be translated
    :return: A string containing the formated code
    """
    prompt = store_prompts.store_prompt_simple(to_translate, PATH_TO_FORMAT_CODE, 'Formatted:')
    answer, prompt = gpt3(prompt, response_length=1024, stop_seq=['Unformatted'])
    return answer


def translate_regular_factors_code_to_text(to_translate: str) -> str:
    """
    Translates the regular factors code into English using the GPT-3 API
    :param to_translate: The code to be translated
    :return: A string containing the English translation
    """
    prompt = store_prompts.store_prompt_regular_factors_code(to_translate, PATH_TO_REGULAR_PROMPTS_CODE)
    answer, prompt = gpt3(prompt,
                          temperature=0,
                          frequency_penalty=0,
                          presence_penalty=0,
                          start_text='',
                          restart_text='',
                          stop_seq=['Code'])
    stripped_answer = answer.replace("\n\n", "")
    return stripped_answer


def translate_regular_factors_text_to_code(to_translate: str) -> str:
    """
    Translates the regular factors text into code using the GPT-3 API
    :param to_translate: The text to be translated
    :return: A string containing the code
    """
    prompt = store_prompts.store_prompt_regular_factors_text(to_translate, PATH_TO_REGULAR_PROMPTS_TEXT)
    answer, prompt = gpt3(prompt, stop_seq=['Text'])
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


def translate_derived_factors_code_to_text(to_translate: str):
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
        prompt = store_prompts.store_prompt_derived_factors(to_translate, PATH_TO_DERIVED_PROMPTS_CODE, i)
        answer, prompt = gpt3(prompt, stop_seq=['Code'])
        stripped_answer = answer.replace("\n\n", "")
        stripped_answer = stripped_answer.replace("\n", "")
        full_answer += " " + stripped_answer

    return full_answer


def translate_derived_factors_text_to_code(to_translate: str) -> str:
    """
    Translates the derived factor text to code using the GPT-3 API
    :param to_translate: The text to be translated
    :return: A string containing the code
    """
    text = extract.extract_derived_factor(to_translate)
    num_derived_factors = extract.get_num_derived_factors(text)
    full_answer = ""

    for i in range(num_derived_factors):
        prompt = store_prompts.store_prompt_derived_factors_text(to_translate, PATH_TO_DERIVED_PROMPTS_TEXT, i)
        answer, prompt = gpt3(prompt, stop_seq=['Text'])
        full_answer += "##\n" + answer

    return full_answer


def translate_counterbalancing_code_to_text(to_translate: str):
    """
    A function that translates the counterbalancing scheme into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the counterbalancing scheme
    """
    _ = store_prompts.store_prompt_balancing(to_translate, PATH_TO_COUNTERBALANCING_PROMPTS_CODE)
    prompt = util.get_code_without_functions(_)
    answer, prompt = gpt3(prompt, response_length=1024, stop_seq=['Code'])
    stripped_answer = answer.replace("\n\n", "")
    return stripped_answer


def translate_counterbalancing_text_to_code(to_translate: str, factors: str):
    """
    A function that translates the counterbalancing scheme into English using
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the counterbalancing scheme
    """
    prompt = store_prompts.store_prompt_balancing_text(to_translate, factors, PATH_TO_COUNTERBALANCING_PROMPTS_TEXT)
    answer, prompt = gpt3(prompt, stop_seq=['Text'])
    stripped_answer = answer.replace("\n\n", "")
    return stripped_answer


def code_to_text(to_translate: str, txt_file_name: str = None, pdf_file_name: str = None) -> str:
    """
    A function that translates the sweetpea code into English using
    the GPT-3 API

    Arguments:
        to_translate: The code to be translated

    Returns:
        A string containing the English translation of the sweetpea code
    """
    util.log(f"Translating sweetpea code...")
    util.log("Translating regular factors...")
    translation = translate_regular_factors_code_to_text(to_translate)
    util.log("Translating derived factors...")
    translation += " " + translate_derived_factors_summary(to_translate)
    translation += " " + translate_derived_factors_code_to_text(to_translate)
    util.log("Translating counterbalancing scheme...")
    translation += " " + translate_counterbalancing_code_to_text(to_translate)

    util.log("Formatting translation...")
    # remove all line breaks from translation
    translation = translation.replace("\n", "")

    # remove double spaces from translation
    translation = translation.replace("  ", " ")

    # write to files
    if txt_file_name:
        util.write_to_text(translation, txt_file_name)

    if pdf_file_name:
        util.write_to_pdf(translation, pdf_file_name)

    util.log("Translation complete.")
    return translation


def text_to_code(to_translate: str, txt_file_name: str = None, py_file_name: str = None,
                 store_sequence_path: str = None) -> str:
    """
    Translates text to sweetPea code
    :param to_translate: the string or file to translate
    :param export_txt: should result be stored as *.txt
    :param export_py: should result be stored as *.py
    :param add_imports: should imports be added to code
    :param out_path: the path to store the file to
    :param store_sequence_path: the path where sequence should be stored
    :return: code as string
    """
    # create a temporary file if to_translate is not a path

    util.log("Translating text...")
    translation = ''

    util.log("Translating regular factors...")
    translation += "### REGULAR FACTORS\n"
    translation += translate_regular_factors_text_to_code(to_translate)

    util.log("Translating derived factors...")
    translation += "### DERIVED FACTORS\n"
    translation += translate_derived_factors_text_to_code(to_translate)
    util.log("Translating counterbalancing scheme...")
    translation += '### EXPERIMENT\n'
    factors = post_process.get_factors_from_code_full(translation)
    translation += translate_counterbalancing_text_to_code(to_translate, factors)
    translation += f'design = {post_process.get_factors_from_code(translation)}\n'
    translation += f'block = {post_process.get_block_from_code(translation)}\n'

    translation += "experiments = synthesize_trials(block, 1)\n"
    translation += '### END OF EXPERIMENT DESIGN'

    if txt_file_name:
        util.write_to_text(translation, txt_file_name)

    if py_file_name:
        # add imports
        _translation = 'from sweetpea import *\n'

        _translation += translation
        if store_sequence_path:
            _translation += f'\nsave_experiments_csv(block, experiments,"{store_sequence_path}")'

        util.write_to_py(_translation, py_file_name)

    util.log("Translation complete.")
    return translation


def text_to_code_sbet(to_translate: str, in_sweet_pea: str = PATH_SWEET_PEA_TMP,
                      in_sequence_pea: str = PATH_SEQUENCE_TMP, py_file_name: str = None,
                      prompt_file_name: str = None) -> str:
    """
    Translates text to sweetPea code
    :param to_translate: the string or file to translate
    :param store_sequence_path: the path where sequence should be stored
    :return: code as string
    """
    # create a temporary file if to_translate is not a path
    util.log("Translating text to sbet...")
    translation = '### REGULAR STIMULI\n'
    util.log("Translating regular stimuli...")
    prompt = to_translate + '\nFACTORS(preamble to regular and conditional):\n'
    factors = None
    if in_sweet_pea:
        factors = util.get_factors_from_file(in_sweet_pea)
        prompt += factors + '\nSTIMULI(preamble to trial block):\n'
    translation += translate_regular_to_code_sbet(to_translate, factors)
    util.log("Translating conditional stimuli...")
    translation += '### CONDITIONAL STIMULI\n'
    translation += translate_conditional_to_code_sbet(to_translate, factors)
    util.log("Translating trial blocks...")
    translation += '### TRIAL BLOCK\n'
    stimuli = util.get_stimuli(translation)
    prompt += stimuli
    translation += translate_trial_block_to_code_sbet(to_translate, stimuli)
    util.log("Translation complete.")
    if py_file_name:
        write = 'from sweetbean import *\n'
        write += 'from sweetbean.primitives import *\n'
        write += 'from numpy import nan\n'
        write += f'trial_sequence = TrialSequence({str(util.get_sequece(in_sequence_pea))})\n'
        write += translation + '\n'
        write += util.out_to_js()
        util.write_to_py(write, py_file_name)
    if prompt_file_name:
        util.write_to_text(prompt, prompt_file_name)


    return translation


def text_to_formatted(to_translate: str, txt_file_name: str = None, pdf_file_name: str = None) -> str:
    """
    A function that translates text to formatted rext
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the sweetpea code
    """
    util.log("Translating unformated text...")
    translation = translate_text_to_formatted(to_translate)

    util.log("Formatting translation...")
    # remove all line breaks from translation
    translation = translation.replace("\n\n", "\n")

    # remove double spaces from translation
    translation = translation.replace("  ", " ")

    if txt_file_name:
        util.write_to_text(translation, txt_file_name)

    if pdf_file_name:
        util.write_to_pdf(translation, pdf_file_name)

    util.log("Translation complete.")

    return translation


def code_to_formatted(to_translate: str, txt_file_name: str = None, py_file_name: str = None) -> str:
    """
    A function that translates code into formatted code
    the GPT-3 API

    Arguments:
        to_translate: the code to be translated

    Returns:
        A string containing the English translation of the sweetpea code
    """
    util.log("Translating unformatted code...")
    translation = translate_code_to_formatted(to_translate)

    print("Formatting translation...")
    # remove all line breaks from translation
    translation = translation.replace("\n\n", "\n")

    if txt_file_name:
        util.write_to_text(translation, txt_file_name)

    if py_file_name:
        util.write_to_py(translation, py_file_name)
    print("Translation complete.")
    return translation

if __name__ == '__main__':
    print(str(util.get_sequece(PATH_SEQUENCE_TMP)))