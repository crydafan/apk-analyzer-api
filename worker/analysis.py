from typing import IO

from androguard.core.apk import APK


def analize_apk(filename: str):
    apk = APK(filename)

    print(apk.get_package())
    print(apk.get_permissions())

    return {"analysis": "This is a mock analysis result."}
