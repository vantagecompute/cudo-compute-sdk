---
title: Installation Guide
description: Install and configure the Cudo Compute SDK
---

# Installation Guide

This guide covers installing the Cudo Compute SDK and setting up authentication.

## Prerequisites

- Python 3.12 or higher
- pip or uv package manager
- A Cudo Compute account with an API key

## Installation Methods

### Using pip

```bash
pip install cudo-compute-sdk
```

### Using uv (Recommended)

```bash
# Install uv if you haven't already
pip install uv

# Install the SDK
uv pip install cudo-compute-sdk
```

### From Source

For development or to use the latest unreleased features:

```bash
git clone https://github.com/vantagecompute/cudo-compute-sdk
cd cudo-compute-sdk

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
uv sync
```

## Obtaining an API Key

To use the Cudo Compute SDK, you need an API key:

1. Log in to the [Cudo Compute Console](https://console.cudo.org/)
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Give your key a descriptive name
5. Copy the generated API key (it will only be shown once)
6. Store it securely

## Configuration

### Environment Variable (Recommended)

Store your API key in an environment variable:

```bash
export CUDO_API_KEY="your-api-key-here"
```

Add this to your `.bashrc`, `.zshrc`, or `.env` file for persistence.

### Direct Initialization

Alternatively, pass the API key directly when initializing the SDK:

```python
from cudo_compute_sdk import CudoComputeSDK

sdk = CudoComputeSDK(api_key="your-api-key-here")
```

### Using python-dotenv

For managing environment variables in development:

```bash
pip install python-dotenv
```

Create a `.env` file:

```bash
CUDO_API_KEY=your-api-key-here
```

In your Python code:

```python
import os
from dotenv import load_dotenv
from cudo_compute_sdk import CudoComputeSDK

load_dotenv()

sdk = CudoComputeSDK(api_key=os.getenv("CUDO_API_KEY"))
```

## Verifying Installation

Test that the SDK is installed and working:

```python
import asyncio
from cudo_compute_sdk import CudoComputeSDK

async def verify():
    sdk = CudoComputeSDK(api_key="your-api-key")
    try:
        projects = await sdk.list_projects()
        print(f"✓ SDK working! Found {len(projects)} projects.")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await sdk.close()

asyncio.run(verify())
```

## Next Steps

- [Usage Examples](./usage) – Learn how to use the SDK
- [API Reference](./api-reference) – Explore available methods
- [Troubleshooting](./troubleshooting) – Get help with common issues
