from typing import Optional
import langcodes

class LanguageMapper:
    """
    Uses the langcodes library to convert language strings to normalized 
    ISO 639-1 strings, handling regional variants like zh-CN.
    """
    # exclude Bosnian and Malay
    EXCLUDED_CODES = {'bs', 'ms'}

    @classmethod
    def get_iso_code_639_1(cls, code: str) -> Optional[str]:
        """
        Converts a language code string to its ISO 639-1 two-letter code.

        :param code: Language code string (e.g., 'zh-CN', 'en_US', 'en')
        :type code: str
        :return: Two-letter ISO 639-1 code (e.g., 'zh', 'en'), or None if the code is invalid, excluded, or empty
        :rtype: Optional[str]
        """
        if not code:
            return None

        try:
            # langcodes.get() parses 'zh-CN', 'en_US', etc.
            lang = langcodes.get(code)

            # .language returns the two-letter ISO 639-1 code (e.g., 'zh')
            iso_code = lang.language

            if iso_code in cls.EXCLUDED_CODES:
                return None
            return iso_code

        except langcodes.LanguageTagError:
            # Returns None if the input is complete gibberish
            return None
