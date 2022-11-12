def extract_segments(filename: str, reg_fac_line: str, stop_fac_line: str) -> str:
    """
    A function that extracts SweetPea code for the definition of regular factors from
    a file

    Arguments:
        filename: the name of the file containing the SweetPea code
        reg_fac_line: the keyword used to identify a section of the code

    Returns:
        A string containing the SweetPea code for a given section
    """

    segments = []
    extracted_code_segment = ""

    with open(filename, 'r') as f:
        read = False
        for line in f:
            if read:
                read = not stop_fac_line in line
                if read:
                    extracted_code_segment += line
                else:
                    segments.append(extracted_code_segment)
                    extracted_code_segment = ""
            if not read:
                read = reg_fac_line in line

    return segments
