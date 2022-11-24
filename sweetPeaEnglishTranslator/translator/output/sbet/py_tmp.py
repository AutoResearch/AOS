from sweetbean import *
from sweetbean.primitives import *
from numpy import nan
trial_sequence = TrialSequence([{'color': 'green', 'word': 'green', 'congruency': 'congruent', 'congruency transition': 'null'}, {'color': 'red', 'word': 'green', 'congruency': 'incongruent', 'congruency transition': 'switch'}, {'color': 'green', 'word': 'green', 'congruency': 'congruent', 'congruency transition': 'switch'}, {'color': 'green', 'word': 'red', 'congruency': 'incongruent', 'congruency transition': 'switch'}, {'color': 'red', 'word': 'green', 'congruency': 'incongruent', 'congruency transition': 'repeat'}, {'color': 'green', 'word': 'red', 'congruency': 'incongruent', 'congruency transition': 'repeat'}, {'color': 'red', 'word': 'red', 'congruency': 'congruent', 'congruency transition': 'switch'}, {'color': 'red', 'word': 'red', 'congruency': 'congruent', 'congruency transition': 'repeat'}, {'color': 'green', 'word': 'green', 'congruency': 'congruent', 'congruency transition': 'repeat'}])
### REGULAR STIMULI
fixation = FixationStimulus(duration=500)
color_word = TextStimulus(duration=1500, text=TimelineVariable('word'), color=TimelineVariable('color'))
feedback = FeedbackStimulus(duration=1500, on_correct=False)
intertrial_interval = BlankStimulus(duration=1500)

### CONDITIONAL STIMULI
def is_correct_c(color):
    return color == 'red'
def is_correct_n(color):
    return color == 'green'
correct_c = DerivedLevel('c', is_correct_c, [TimelineVariable('color')])
correct_n = DerivedLevel('n', is_correct_n, [TimelineVariable('color')])
correct = DerivedParameter('correct', [correct_c, correct_n])
color_word = TextStimulus(duration=1500, text=TimelineVariable('word'), color=TimelineVariable('color'), correct=correct, choices=['c', 'n'])
### TRIAL BLOCK
trial_block = TrialBlock([fixation, color_word, feedback, intertrial_interval], trial_sequence)
experiment = Experiment([trial_block])

text = experiment.to_psych()
with open("sweetPeaEnglishTranslator/translator/output/sbet/out.js", "w") as f:
    f.write(text)
