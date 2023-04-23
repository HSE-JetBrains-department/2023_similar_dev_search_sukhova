from enry import get_language, is_binary


class LanguageExtractor:
    @classmethod
    def extract_language(cls, file_name: str, file_content: bytes):
        """
        Extract language from file by name and content.
        :param file_name: Name of file.
        :param file_content: Content of file.
        :return: Language of file content.
        """
        language = get_language(filename=file_name, content=file_content)
        if not language and is_binary(file_content):
            language = "binary"
        elif not language:
            language = "undefined"
        return language
