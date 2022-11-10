import prompt_scrambling, util

codes_segment_1 = 'color      = factor("color", ["red", "green", "blue", "brown"])\n' \
                  'word = factor("word", ["red", "green", "blue", "brown"])'

prompt_segment_1 = 'There are two regular factors: color and word. The color factor consists of four levels: "red", "green", "blue", "brown". The word factor also consists of the four levels: "red", "green", "blue", "brown".'

code_segments_regular = util.extract_segments('../gpt3prompt_regular_factors_code.txt', 'Code:', 'Text:')
text_segments_regular = util.extract_segments('../gpt3prompt_regular_factors_code.txt', 'Text:', 'Code:')

code_segments_derived = util.extract_segments('../gpt3prompt_derived_factors_code.txt', 'Code:', 'Text:')
text_segments_derived = util.extract_segments('../gpt3prompt_derived_factors_code.txt', 'Text:', 'Code:')

code_segments_counterbalancing = util.extract_segments('../gpt3prompt_counterbalancing.txt', 'Code:', 'Text:')
text_segments_counterbalancing = util.extract_segments('../gpt3prompt_counterbalancing.txt', 'Text:', 'Code:')



print(len(code_segments_regular), len(text_segments_regular))
print(len(code_segments_derived), len(text_segments_derived))
print(len(code_segments_counterbalancing), len(text_segments_counterbalancing))




def write_to_file(path,code_segments, text_segments):
    f = open(path, "a")
    for c, t in zip(code_segments, text_segments):
        c_s, t_s = prompt_scrambling.scramble_prompt(c, t)
        f.write('Code:\n')
        f.write(c_s)
        f.write('Text:\n')
        f.write(t_s)
    f.close()

write_to_file('regular_scrambled.txt', code_segments_regular, text_segments_regular)
write_to_file('derived_scrambled.txt', code_segments_derived, text_segments_derived)
write_to_file('counterbalancing_scrambled.txt', code_segments_counterbalancing, text_segments_counterbalancing)

