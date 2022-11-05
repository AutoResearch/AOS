import promt_scrambling
from sweetpea.primitives import factor, Factor

codes_segment_1 = 'color      = factor("color", ["red", "green", "blue", "brown"])\n' \
                  'word = factor("word", ["red", "green", "blue", "brown"])'

prompt_segment_1 = 'There are two regular factors: color and word. The color factor consists of four levels: "red", "green", "blue", "brown". The word factor also consists of the four levels: "red", "green", "blue", "brown".'

code_segment_1_scrambled, prompt_segment_1_scrambled = promt_scrambling.scrambling_regular_factor(codes_segment_1, prompt_segment_1)

print(codes_segment_1)
print(prompt_segment_1)
print(code_segment_1_scrambled)
print(prompt_segment_1_scrambled)

color = Factor("color", ["red", "green", "blue", "brown"])
word = factor("word", ["red", "green", "blue", "brown"])
