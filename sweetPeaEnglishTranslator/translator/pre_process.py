def check_for_line_comments(to_check: str) -> bool:
    """
    Checks a file for line comments (in python style, aka lines that start with #
    :param to_check: A file to check
    :return: True if there are line comments, False if not
    """
    with open(to_check) as file:
        for line in file:
            if line.startswith('#'):
                return True
    return False


def _remove_line_comments(to_process: str, to_file: str = None) -> str:
    """
    Removes lines starting with # from file
    :param to_process: The file to process
    :param to_file The file to write to
    :return The path to the processed file
    """
    with open(to_process) as f:
        lines = [line for line in f]
    if not to_file:
        to_file = to_process
    with open(to_file, 'w') as f:
        for line in lines:
            if not line.startswith('#'):
                f.write(line)
    return to_file


def _remove_empty_lines(to_process: str, to_file: str = None) -> str:
    """
    Remove empty lines (lines == '\n' from file)
    :param to_process: The file to process
    :param to_file The file to write to
    :return The path to the processed file
    """
    with open(to_process) as f:
        lines = [line for line in f]

    if not to_file:
        to_file = to_process
    with open(to_file, 'w') as f:
        for line in lines:
            if not line.startswith('\n'):
                f.write(line)
    return to_file


def _remove_line_breaks(to_process: str, to_file: str = None) -> str:
    """
    Remove empty linebreaks from file
    :param to_process: The file to process
    :param to_file The file to write to
    :return The path to the processed file
    """
    with open(to_process) as f:
        text = f.read()

    if not to_file:
        to_file = to_process
    with open(to_file, 'w') as f:
        f.write(text.replace('\n', ' '))
    return to_file


def preprocess_text(to_process: str, to_file: str = None, is_return_path: bool = False) -> str:
    """
        Remove empty line comments and empty lines (lines == '\n' from file)
        :param to_process: The file to process
        :param to_file The file to write to
        :param is_return_path: If True, return a path
        :return The path to the processed file or the text as string
        """
    if not to_file:
        to_file = to_process
    to_file = _remove_line_comments(to_process, to_file)
    to_file = _remove_empty_lines(to_file, to_file)
    to_file = _remove_line_breaks(to_file, to_file)
    if is_return_path:
        return to_file
    with open(to_file) as f:
        return f.read()
