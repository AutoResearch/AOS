import os

_dirname = os.path.dirname(__file__)
# prompts for code to text
PATH_TO_REGULAR_PROMPTS_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors_code.txt')
PATH_TO_DERIVED_PROMPTS_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_derived_factors_code.txt')
PATH_TO_COUNTERBALANCING_PROMPTS_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_counterbalancing_code.txt')

# prompts for text to code
PATH_TO_REGULAR_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/gpt3prompt_regular_factors_text.txt')
PATH_TO_DERIVED_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/gpt3prompt_derived_factors_text.txt')
PATH_TO_COUNTERBALANCING_PROMPTS_TEXT = os.path.join(_dirname, 'prompts/gpt3prompt_counterbalancing_text.txt')

# prompts for format
PATH_TO_FORMAT_TEXT = os.path.join(_dirname, 'prompts/gpt3prompt_format_text.txt')
PATH_TO_FORMAT_CODE = os.path.join(_dirname, 'prompts/gpt3prompt_format_code.txt')

# key words in code
TRANSITION_STRINGS = ("Transition(", "transition(")
WITHIN_TRIAL_STRINGS = ("WithinTrial(", "within_trial(")
WINDOW_STRINGS = ("Window(", "window(")
NON_CHARACTERS = (" ", ",", "(", ")", "[", "]", ":", ";")
DERIVED_LEVEL_STRINGS = ("DerivedLevel", "derived_level")
FACTOR_STRINGS = ("Factor", "factor")

# hash formatting
REGULAR_FACTORS = "### REGULAR FACTORS"
DERIVED_FACTORS = "### DERIVED FACTORS"
BALANCING = "### EXPERIMENT"
END_OF_SWEETPEA_CODE = "### END OF EXPERIMENT DESIGN"
