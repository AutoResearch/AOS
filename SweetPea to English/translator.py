from translate import translate_sweetpea_code


if __name__ == '__main__':
    # to_translate = "unextracted_code.py"
    # translation = "Translation: " + translate_regular_factors(to_translate)
    # translation = "Translation: " + translate_derived_factors_summary(to_translate)
    # translation = "Translation: " + translate_derived_factors(to_translate)
    # translation = "Translation: " + translate_counterbalancing(to_translate)
    # display_typed_text(translation)
    test_string = '### REGULAR FACTORS\n' \
                  'object = Factor("object identity", [Level("H", 2), Level("S", 1)])\n' \
                  'motion = Factor("motion", [Level("left", 2), Level("right", 3)])\n' \
                  '### DERIVED FACTORS\n' \
                  'def response_left(object):\n' \
                  '    return object == "H"\n' \
                  'def response_right(object):\n' \
                  '    return object == "S"\n' \
                  'response = Factor("correct response", [' \
                  'DerivedLevel("left", WithinTrial(response_left, [object])),' \
                  'DerivedLevel("right", WithinTrial(response_right, [object])),])\n' \
                  '### EXPERIMENT\n' \
                  'constraints = [at_most_k_in_a_row(5, response),' \
                  'minimum_trials(100)]\n' \
                  'design = [object, motion, response]\n' \
                  'crossing = [object, motion,]\n' \
                  'block = fully_cross_block(design, crossing, constraints)\n' \
                  'experiments = synthesize_trials_non_uniform(block, 1)\n' \
                  '### END OF EXPERIMENT DESIGN\n' \
                  'print_experiments(block, experiments)'

    to_translate = "test\code_1.py"
    translation = "Translation: " + translate_sweetpea_code(to_translate, export_pdf=True)
    print(translation)
