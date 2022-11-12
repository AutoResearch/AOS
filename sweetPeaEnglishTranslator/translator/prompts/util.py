def switch_prompts(path):
    """
    utility function to switch prompts
    :param path:
    :return:
    """
    current_str = ""
    code = []
    text = []
    res = ""
    with open(path) as file:
        i = 0
        code_to_text = False
        for line in file:
            if line.startswith("Code:"):
                if current_str:
                    text.append(current_str)
                    current_str = ""
                if i == 0:
                    code_to_text = True
            if line.startswith("Text:"):
                if current_str:
                    code.append(current_str)
                    current_str = ""
            current_str += line
            i += 1

        for c, t in zip(code, text):
            if code_to_text:
                res += t
                res += c
            else:
                res += c
                res += t
    f = open("prompt_new.text", "w")
    f.write(res)
    f.close()

def to_lower(path):
    text_lower = ''
    with open(path) as f:
        text_lower += f.read().lower()
    with open(path, 'w') as f:
        f.write(text_lower)

if __name__ == '__main__':
    to_lower("gpt3prompt_format_text.txt")
