from sweetpea import *
### REGULAR FACTORS
color = Factor("color",  ["red", "green"])
word = Factor("word", ["red", "green"])
### DERIVED FACTORS
### EXPERIMENT
constraints = []
crossing = [color]
design = [color, word]
block = CrossBlock(design, crossing, constraints, require_complete_crossing=False)
experiments = synthesize_trials(block, 1)
### END OF EXPERIMENT DESIGN
save_experiments_csv(block, experiments,"sweetPeaEnglishTranslator/translator/output/spet/younes/seq_tmp")