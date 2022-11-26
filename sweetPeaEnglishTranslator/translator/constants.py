import os

_dirname = os.path.dirname(__file__)
# prompts for code to text
PATH_TO_REGULAR_PROMPTS_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors_code.txt')
PATH_TO_DERIVED_PROMPTS_CODE = os.path.join(_dirname, 'prompts/spet/derived_code.txt')
PATH_TO_COUNTERBALANCING_PROMPTS_CODE = os.path.join(_dirname, 'prompts/spet/design_code.txt')

## prompts for text to code
PATH_TO_REGULAR_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors_text.txt')
PATH_TO_DERIVED_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/spet/derived_text.txt')
PATH_TO_COUNTERBALANCING_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/spet/design_text.txt')

# sbet
PATH_REGULAR_TEXT_SBET = os.path.join(_dirname, 'prompts/sbet/regular_text.txt')
PATH_CONDITIONAL_TEXT_SBET = os.path.join(_dirname, 'prompts/sbet/conditional_text.txt')
PATH_TRIAL_BLOCK_TEXT_SBET = os.path.join(_dirname, 'prompts/sbet/trial_block_text.txt')

## prompts for format
PATH_TO_FORMAT_TEXT = os.path.join(_dirname, 'prompts/spet/format_text.txt')
PATH_TO_FORMAT_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_format_code.txt')


# sbet
PATH_FORMAT_TEXT_SBET = os.path.join(_dirname, 'prompts/sbet/format_text.txt')

# key words in code
TRANSITION_STRINGS = ("Transition(", "transition(")
WITHIN_TRIAL_STRINGS = ("WithinTrial(", "within_trial(")
WINDOW_STRINGS = ("Window(", "window(")
NON_CHARACTERS = (" ", ",", "(", ")", "[", "]", ":", ";")
DERIVED_LEVEL_STRINGS = ("DerivedLevel", "derived_level")
FACTOR_STRINGS = ("Factor", "factor")

## hash formatting
REGULAR_FACTORS = "### REGULAR FACTORS"
DERIVED_FACTORS = "### DERIVED FACTORS"
BALANCING = "### EXPERIMENT"
END_OF_SWEETPEA_CODE = "### END OF EXPERIMENT DESIGN"

# spet
REGULAR_STIMULI_SPET = "### REGULAR STIMULI"
CONDITIONAL_STIMULI_SPET = "### CONDITIONAL STIMULI"
TRIAL_BLOCK_SPET = "### TRIAL BLOCK"
END_SPET = "### END"

#
PATH_SWEET_PEA_TMP = os.path.join(_dirname, 'output/spet/py_tmp.py')
PATH_SEQUENCE_TMP = os.path.join(_dirname, 'output/spet/seq_tmp_0.csv')
