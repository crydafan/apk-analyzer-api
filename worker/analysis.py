from loguru import logger

from androguard.misc import AnalyzeAPK

logger.disable("androguard")
logger.disable("androguard.core")
logger.disable("androguard.misc")


def analize_apk(filename: str):
    api_keys_found: list[str] = []

    _a, d, _dx = AnalyzeAPK(filename)

    # Look for strings that resemble API keys in the DEX files
    for dex in d:
        strings = dex.get_strings()
        for s in strings:
            if "sk-" in s:
                api_keys_found.append(s)

    return {"analysis": {"api_keys_found": api_keys_found}}
