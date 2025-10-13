---
title: Troubleshooting
description: Common issues and solutions for Cudo Compute SDK
---

# Troubleshooting

Quick solutions for common issues when using the Cudo Compute SDK.

## Authentication Errors

### 401 Unauthorized

**Symptom**: API requests fail with `401 Unauthorized`

**Causes**:
- Invalid or expired API key
- API key not properly set

**Solutions**:

1. Verify your API key is correct:
```python
sdk = CudoComputeSDK(api_key="your-actual-api-key")
```

2. Check environment variable:
```bash
echo $CUDO_API_KEY
```

3. Generate a new API key from the [Cudo Compute Console](https://console.cudo.org/)

### 403 Forbidden

**Symptom**: API requests fail with `403 Forbidden`

**Cause**: API key doesn't have permission for the requested resource

**Solution**: Check your API key permissions in the Cudo Compute Console

## Connection Errors

### Connection Timeout

**Symptom**: Requests hang or timeout

**Solutions**:

1. Check network connectivity:
```bash
curl -I https://rest.compute.cudo.org
```

2. Increase timeout:
```python
sdk = CudoComputeSDK(api_key="...")
sdk.client.timeout = httpx.Timeout(60.0)
```

3. Check firewall rules

### SSL Certificate Errors

**Symptom**: SSL verification errors

**Solution**: Ensure your system has up-to-date CA certificates:
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates

# macOS
brew upgrade openssl
```

## Resource Not Found Errors

### 404 Not Found

**Symptom**: Getting VM or other resources fails with 404

**Solutions**:

1. Verify the resource ID:
```python
vms = await sdk.list_vms(project_id="your-project")
for vm in vms:
    print(f"VM ID: {vm.id}")
```

2. Check the project ID is correct

3. Ensure resource hasn't been deleted

## Validation Errors

### Pydantic Validation Error

**Symptom**: `ValidationError` when parsing API responses

**Cause**: API response doesn't match expected schema

**Solutions**:

1. Update to the latest SDK version:
```bash
pip install --upgrade cudo-compute-sdk
```

2. Check API response:
```python
try:
    vm = await sdk.get_vm(project_id="...", vm_id="...")
except Exception as e:
    print(f"Error: {e}")
    print(f"Response: {e.response.json()}")  # If HTTPStatusError
```

## VM Creation Issues

### Insufficient Quota

**Symptom**: VM creation fails with quota error

**Solution**: Check your account quotas in the Cudo Compute Console or contact support

### Invalid Machine Type

**Symptom**: VM creation fails with invalid machine type

**Solution**: List available machine types for the data center:
```python
machine_types = await sdk.list_machine_types_for_data_center(
    data_center_id="gb-bournemouth-1"
)
for mt in machine_types:
    print(f"{mt.machine_type}: {mt.vcpus} vCPUs, {mt.memory_gib}GB RAM")
```

### Invalid Image

**Symptom**: VM creation fails with invalid image ID

**Solution**: List available images:
```python
images = await sdk.list_images()
for image in images:
    print(f"{image.id}: {image.os_name} {image.os_version}")
```

## Async/Await Issues

### RuntimeError: asyncio.run() cannot be called from a running event loop

**Symptom**: Error when using `asyncio.run()` in Jupyter or async context

**Solution**: Use `await` directly instead:
```python
# In Jupyter/IPython
sdk = CudoComputeSDK(api_key="...")
vms = await sdk.list_vms(project_id="...")
```

### Not Closing SDK Properly

**Symptom**: ResourceWarning about unclosed client

**Solution**: Always close the SDK:
```python
async def main():
    sdk = CudoComputeSDK(api_key="...")
    try:
        # your code
        pass
    finally:
        await sdk.close()
```

Or use async context manager pattern:
```python
class CudoComputeSDKContext:
    def __init__(self, api_key: str):
        self.sdk = CudoComputeSDK(api_key)
    
    async def __aenter__(self):
        return self.sdk
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.sdk.close()

# Usage
async with CudoComputeSDKContext(api_key="...") as sdk:
    vms = await sdk.list_vms(project_id="...")
```

## Rate Limiting

### 429 Too Many Requests

**Symptom**: API requests fail with `429 Too Many Requests`

**Solution**: Implement exponential backoff:
```python
import asyncio
from httpx import HTTPStatusError

async def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except HTTPStatusError as e:
            if e.response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Rate limited, waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
            else:
                raise

# Usage
vms = await with_retry(lambda: sdk.list_vms(project_id="..."))
```

## Installation Issues

### ImportError: No module named 'cudo_compute_sdk'

**Solution**:
```bash
pip install cudo-compute-sdk
# or
uv pip install cudo-compute-sdk
```

### Version Conflicts

**Solution**: Use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install cudo-compute-sdk
```

## Debugging

### Enable Logging

Get detailed debug information:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable httpx logging
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Inspect HTTP Requests

```python
import httpx

# Create client with event hooks
async def log_request(request):
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")

async def log_response(response):
    print(f"Response: {response.status_code}")
    print(f"Body: {response.text}")

client = httpx.AsyncClient(
    event_hooks={
        'request': [log_request],
        'response': [log_response]
    }
)

sdk = CudoComputeSDK(api_key="...")
sdk.client = client
```

## Getting Help

If you're still experiencing issues:

1. **Check the GitHub Issues**: [github.com/vantagecompute/cudo-compute-sdk/issues](https://github.com/vantagecompute/cudo-compute-sdk/issues)

2. **Open a New Issue**: Include:
   - Python version (`python --version`)
   - SDK version (`pip show cudo-compute-sdk`)
   - Minimal code to reproduce the issue
   - Full error traceback
   - **Never include your API key**

3. **Contact Cudo Compute Support**: For account-specific issues

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `401 Unauthorized` | Invalid API key | Check API key |
| `403 Forbidden` | Insufficient permissions | Verify API key permissions |
| `404 Not Found` | Resource doesn't exist | Verify resource ID |
| `422 Unprocessable Entity` | Invalid request parameters | Check parameter values |
| `429 Too Many Requests` | Rate limit exceeded | Implement retry with backoff |
| `500 Internal Server Error` | API server error | Retry or contact support |
| `503 Service Unavailable` | API temporarily unavailable | Retry after a delay |
