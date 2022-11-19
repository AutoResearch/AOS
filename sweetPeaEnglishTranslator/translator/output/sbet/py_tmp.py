### REGULAR STIMULI
fixation = FixationStimulus(duration=500)
color_word = TextStimulus(duration=1500, text=TimelineVariable('word'), color=TimelineVariable('color'))
intertrial_interval = BlankStimulus(duration=1500)
feedback = FeedbackStimulus(duration=1500, on_correct=False)

### CONDITIONAL STIMULI
def is_correct_c(word):
    return word == 'red'
def is_correct_n(word):
    return word == 'green'
correct_c = DerivedLevel('c', is_correct_c, [TimelineVariable('word')])
correct_n = DerivedLevel('n', is_correct_n, [TimelineVariable('word')])
correct = DerivedParameter('correct', [correct_c, correct_n])
color_word = TextStimulus(duration=1500, text=TimelineVariable('word'), color=TimelineVariable('color'), correct=correct, choices=['c', 'n'])
### TRIAL BLOCK
trial_block = TrialBlock([fixation, color_word, feedback, intertrial_interval])
experiment = Experiment([trial_block])
