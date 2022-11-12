def _extract_segment(filename: str, reg_fac_line: str) -> str:
    """
    A function that extracts text segments
    Arguments:
        filename: the name of the file containing the SweetPea code
        reg_fac_line: the keyword used to identify a section of the code

    Returns:
        A string containing the SweetPea code for a given section
    """
    extracted_code = ""
    file = open(filename)
    line = file.readline().strip()  # initially holds first line of file
    while line != reg_fac_line:
        line = file.readline().strip()  # next line
    if line == reg_fac_line:
        line = file.readline().strip()
        while "###" not in line:  # stops when next # is found
            extracted_code += line + "\n"
            line = file.readline().strip()
    file.close()
    if not extracted_code:
        raise Exception("Error in extract_segment: No segment found")
    return extracted_code

def extract_main(filename: str) -> str:
    """
    A function that extracts the SweetPea code from a SweetPea code file

    Arguments:
        filename: the name of the file containing the SweetPea code

    Returns:
        A string containing the regular factors code
    """
    extracted_code = ""
    file = open(filename)
    line = file.readline()

    # reads in only relevant parts of the code
    while line:
        if line.strip() == REGULAR_FACTORS or line.strip() == DERIVED_FACTORS or line.strip() == BALANCING:
            line = file.readline()
            while line.strip() != REGULAR_FACTORS \
                    and line.strip() != DERIVED_FACTORS \
                    and line.strip() != BALANCING \
                    and line.strip() != END_OF_SWEETPEA_CODE:  # stops when next code section is found
                extracted_code += line.strip() + "\n"
                line = file.readline()

        if line.strip == END_OF_SWEETPEA_CODE:
            break

        if line.strip() != REGULAR_FACTORS and line.strip() != DERIVED_FACTORS and line.strip() != BALANCING:
            line = file.readline()

    # convert code to lines
    extracted_code = extracted_code.split("\n")
    for line in extracted_code:
        if len(line) > 0:
            if line[0] == "#":
                extracted_code.remove(line)

    extracted_code = "\n".join(extracted_code)
    extracted_code = extracted_code.replace("\n\n", "\n")

    return extracted_code
