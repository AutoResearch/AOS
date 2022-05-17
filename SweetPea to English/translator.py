from gpt3 import gpt3

def extract(filename: str) -> str:
    """A function that takes in a string of the line that the is being
    extracted for and a filename of the SweetPea code, returns the parts of the
    code that the to_extract string indicates"""
    reg_fac_line = "### REGULAR FACTORS"
    extracted_code = ""
    file = open(filename)
    line = file.readline().strip()  # initially holds first line of file
    while line != reg_fac_line:
        line = file.readline().strip()  # next line
    if line == reg_fac_line:
        line = file.readline().strip()
        while "###" not in line:  # stops when next ### is found
            # print(line)
            extracted_code += line + "\n"
            line = file.readline().strip()
    file.close()
    return extracted_code

print(extract("unextracted_code.py"))

# CURRENTLY WORKING

# def extract(to_extract: str, filename: str) -> str:
#     """A function that takes in a string of the line that the is being
#     extracted for and a filename of the SweetPea code, returns the parts of the
#     code that the to_extract string indicates"""
#     # reg_fac_line = "### REGULAR FACTORS"
#     extracted_code = ""
#     file = open(filename)
#     line = file.readline().strip()  # initially holds first line of file
#     while line != to_extract:
#         line = file.readline().strip()  # next line
#     if line == to_extract:
#         line = file.readline().strip()
#         while "###" not in line:  # stops when next ### is found
#             # print(line)
#             extracted_code += line + "\n"
#             line = file.readline().strip()
#     file.close()
#     return extracted_code

# print(extract("### REGULAR FACTORS", "unextracted_code.py"))
# print(extract("### DERIVED FACTORS", "unextracted_code.py"))

def store_prompt_rf(sp_filename: str, prompt_filename: str) -> str:
    """A function that stores the GPT-3 prompt and regular factors into a
    single string"""
    stored_string = ""
    with open(prompt_filename) as file:
        for line in file:
            stored_string += line
    stored_string += extract(sp_filename) + "\nText: "
    return stored_string

# print(store_prompt_rf("unextracted_code.py", "gpt3prompt.txt"))

def translate_sweetpea():
    """A function that translates the regular factors code into English using
    the GPT-3 API"""
    to_translate = input("Input sweetpea code file: ")
    prompt = store_prompt_rf(to_translate, "gpt3prompt.txt")
    answer, prompt = gpt3(prompt,
                          temperature=0,
                          frequency_penalty=1,
                          presence_penalty=1,
                          start_text='',
                          restart_text='',
                          stop_seq=['Code'])
    stripped_answer = answer.replace("\n\n", "")
    print('Text: ' + stripped_answer)

if __name__ == '__main__':
    translate_sweetpea()
