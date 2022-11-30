def get_factors_from_code(code: str) -> str:
    lines = code.splitlines()
    design = []
    for line in lines:
        words = line.split()
        if len(words) >= 3 and (words[2].startswith('factor') or words[2].startswith('Factor')):
            design.append(words[0])
    design = str(design)
    design = design.replace("'", "")
    return design

def get_block_from_code(code: str) -> str:
    lines = code.splitlines()
    for line in lines:
        if line.startswith('crossing'):
            words = line.split()
            if len(words) >= 3 and words[2].startswith('[['):
                return 'MultiCrossBlock(design, crossing, constraints, require_complete_crossing=False)'
    return 'CrossBlock(design, crossing, constraints, require_complete_crossing=False)'


def get_factors_from_code_full(code: str) -> str:
    lines = code.splitlines()
    res = ''
    for line in lines:
        words = line.split()
        if len(words) >= 3 and (words[2].startswith('factor') or words[2].startswith('Factor')):
            res += line
    return res
