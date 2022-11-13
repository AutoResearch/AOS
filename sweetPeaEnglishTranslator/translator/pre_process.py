def check_for_line_comments(to_check: str) -> bool:
    """
    Checks a text for line comments (in python style, aka lines that start with #
    :param to_check: A file to check
    :return: True if there are line comments, False if not
    """
    lines = to_check.splitlines()
    for line in lines:
        if line.startswith('#'):
            return True
    return False


def _remove_line_comments(to_process: str) -> str:
    """
    Removes lines starting with # from file
    :param to_process: The file to process
    :return The path to the processed file
    """
    lines = to_process.splitlines(True)
    res = ''
    for line in lines:
        if not line.startswith('#'):
            res += line
    return res


def _remove_empty_lines(to_process: str) -> str:
    """
    Remove empty lines (lines == '\n' from file)
    :param to_process: The file to process
    :return The path to the processed file
    """
    lines = to_process.splitlines(True)
    res = ''
    for line in lines:
        if not line.startswith('\n'):
            res += line
    return res


def _remove_line_breaks(to_process: str) -> str:
    """
    Remove empty linebreaks from file
    :param to_process: The file to process
    :return The path to the processed file
    """
    return to_process.replace('\n', ' ')


def preprocess_text(to_process: str) -> str:
    """
        Remove empty line comments and empty lines (lines == '\n' from file)
        :param to_process: The file to process
        :return The path to the processed file or the text as string
        """
    res = _remove_line_comments(to_process)
    res = _remove_empty_lines(res)
    return _remove_line_breaks(res)


def preprocess_code(to_process: str) -> str:
    res = _remove_line_comments(to_process)
    return _remove_empty_lines(res)
