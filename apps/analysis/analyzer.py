"""
APK Analysis module using androguard.
Add your analysis logic here.
"""

from androguard.core.apk import APK
from loguru import logger

logger.disable("androguard")


def analyze_apk(apk_path: str) -> dict[str, str]:
    """
    Analyze an APK file and extract metadata.
    """
    apk = APK(apk_path)

    # Basic metadata
    result = {
        "package_name": apk.get_package(),
        "app_name": apk.get_app_name(),
        "version_name": apk.get_androidversion_name(),
        "version_code": apk.get_androidversion_code(),
        "min_sdk": apk.get_min_sdk_version(),
        "target_sdk": apk.get_target_sdk_version(),
        "max_sdk": apk.get_max_sdk_version(),
        # Permissions
        "permissions": apk.get_permissions(),
        "declared_permissions": apk.get_declared_permissions(),
        # Components
        "activities": apk.get_activities(),
        "services": apk.get_services(),
        "receivers": apk.get_receivers(),
        "providers": apk.get_providers(),
        # Security info
        "is_signed": apk.is_signed(),
        "is_signed_v1": apk.is_signed_v1(),
        "is_signed_v2": apk.is_signed_v2(),
        "is_signed_v3": apk.is_signed_v3(),
        # Additional metadata
        "main_activity": apk.get_main_activity(),
        "libraries": list(apk.get_libraries()),
        "features": apk.get_features(),
    }

    # Get certificate info if signed
    if apk.is_signed():
        try:
            certs = apk.get_certificates()
            if certs:
                cert = certs[0]
                result["certificate"] = {
                    "issuer": cert.issuer.rfc4514_string(),
                    "subject": cert.subject.rfc4514_string(),
                    "serial_number": str(cert.serial_number),
                    "not_valid_before": cert.not_valid_before_utc.isoformat(),
                    "not_valid_after": cert.not_valid_after_utc.isoformat(),
                }
        except Exception:
            result["certificate"] = None

    return result


"""
def analyze_apk_deep(apk_path: str) -> dict:
    from androguard.misc import AnalyzeAPK

    apk, dex_list, analysis = AnalyzeAPK(apk_path)

    result = analyze_apk(apk_path)

    # Add DEX analysis
    result["classes_count"] = len(list(analysis.get_classes()))
    result["methods_count"] = len(list(analysis.get_methods()))
    result["strings_count"] = len(list(analysis.get_strings()))

    # Detect potential issues (basic example)
    suspicious_permissions = [
        "android.permission.SEND_SMS",
        "android.permission.READ_SMS",
        "android.permission.RECEIVE_SMS",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_CALL_LOG",
        "android.permission.CAMERA",
    ]

    result["suspicious_permissions"] = [
        p for p in result["permissions"] if p in suspicious_permissions
    ]

    return result
"""
