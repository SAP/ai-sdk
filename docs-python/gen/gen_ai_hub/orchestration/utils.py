def load_text_file(file_path):
    """Loads and returns the content of a text file.

    :param file_path: The path to the text file to be loaded.
    :type file_path: str
    :return: The content of the file as a string.
    :rtype: str
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

