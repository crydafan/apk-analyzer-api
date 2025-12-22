# APK Analyzer Service

Python microservice for analyzing Android APK files using [androguard](https://github.com/androguard/androguard).

## Setup

```bash
cd apps/analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# Development
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /health
```

### Analyze APK (upload)
```
POST /analyze
Content-Type: multipart/form-data

file: <apk-file>
```

### Analyze APK (from URL)
```
POST /analyze-url
Content-Type: application/json

{
  "url": "https://bucket.example.com/path/to/app.apk"
}
```

## Docker

```bash
# Build
docker build -t apk-analyzer .

# Run
docker run -p 8000:8000 apk-analyzer
```

## Example Response

```json
{
  "package_name": "com.example.app",
  "app_name": "Example App",
  "version_name": "1.0.0",
  "version_code": "1",
  "min_sdk": "21",
  "target_sdk": "34",
  "permissions": [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE"
  ],
  "activities": ["com.example.app.MainActivity"],
  "services": [],
  "receivers": [],
  "providers": [],
  "is_signed": true,
  "main_activity": "com.example.app.MainActivity"
}
```
