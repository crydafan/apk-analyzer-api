"""
FastAPI application for analyzing Android APK files.
"""

import tempfile

from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from loguru import logger
from androguard.core.apk import APK  # pyright: ignore[reportMissingTypeStubs]

logger.disable("androguard")


def analyze_apk(apk_path: str) -> dict[str, str]:
    """
    Analyze an APK file and extract metadata.
    """
    apk = APK(apk_path)

    # Basic metadata
    result = {  # pyright: ignore[reportUnknownVariableType]
        "package_name": apk.get_package(),
        "app_name": apk.get_app_name(),  # pyright: ignore[reportUnknownMemberType]
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
            certs = (  # pyright: ignore[reportUnknownVariableType]
                apk.get_certificates()  # pyright: ignore[reportUnknownMemberType]
            )
            if certs:
                cert = certs[0]  # pyright: ignore[reportUnknownVariableType]
                result["certificate"] = {
                    "issuer": cert.issuer.rfc4514_string(),  # pyright: ignore[reportUnknownMemberType]
                    "subject": cert.subject.rfc4514_string(),  # pyright: ignore[reportUnknownMemberType]
                    "serial_number": str(cert.serial_number),
                    "not_valid_before": cert.not_valid_before_utc.isoformat(),  # pyright: ignore[reportUnknownMemberType]
                    "not_valid_after": cert.not_valid_after_utc.isoformat(),  # pyright: ignore[reportUnknownMemberType]
                }
        except Exception:
            result["certificate"] = None

    return result  # pyright: ignore[reportUnknownVariableType]


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    print("🐍 APK Analyzer service starting")
    yield
    print("🐍 APK Analyzer service shutting down")


app = FastAPI(
    title="APK Analyzer",
    description="Microservice for analyzing Android APK files",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}


@app.post("/")
async def root(file: UploadFile = File(...)):
    """
    Analyze an uploaded APK file.
    Returns extracted metadata and analysis results.
    """
    if not file.filename or not file.filename.endswith(".apk"):
        raise HTTPException(status_code=400, detail="File must be an APK")

    # Save to temp file for analysis
    with tempfile.NamedTemporaryFile(suffix=".apk") as tmp:
        content = await file.read()
        tmp.write(content)

        try:
            result = analyze_apk(tmp.name)
            return JSONResponse(content=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


"""
@app.post("/analyze-url")
async def analyze_from_url(body: dict):
    import httpx

    url = body.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' field")

    # Download APK to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as tmp:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to download APK")
            tmp.write(response.content)
            tmp_path = tmp.name

    try:
        result = analyze_apk(tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)
"""
