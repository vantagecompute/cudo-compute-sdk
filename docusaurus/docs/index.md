---
title: "Cudo Compute SDK - Overview"
description: "Python SDK for Cudo Compute Cloud Platform"
slug: /
---

# Cudo Compute SDK

The official Python SDK for interacting with the [Cudo Compute](https://www.cudocompute.com/) cloud platform. This SDK provides a comprehensive, type-safe interface to manage virtual machines, data centers, networks, storage, and other cloud resources via the Cudo Compute REST API.

## Features

- **Async/Await Support**: Built on `httpx` for efficient async operations
- **Type Safety**: Comprehensive Pydantic models for all API responses
- **Full API Coverage**: Complete support for Cudo Compute REST API
- **Resource Management**: VMs, networks, storage, security groups, SSH keys
- **Well-Documented**: Type hints and docstrings for all methods

## Quick Start

Install from PyPI:

```bash
pip install cudo-compute-sdk
```

Or using `uv`:

```bash
uv pip install cudo-compute-sdk
```

### Basic Usage

```python
import asyncio
from cudo_compute_sdk import CudoComputeSDK

async def main():
    # Initialize SDK with your API key
    sdk = CudoComputeSDK(api_key="your-api-key-here")
    
    try:
        # List all projects
        projects = await sdk.list_projects()
        print(f"Found {len(projects)} projects")
        
        # List VMs in a project
        vms = await sdk.list_vms(project_id="my-project")
        for vm in vms:
            print(f"VM: {vm.id} - Status: {vm.state}")
            
    finally:
        await sdk.close()

asyncio.run(main())
```

## What is Cudo Compute?

Cudo Compute is a distributed cloud computing platform that provides:

- **GPU & CPU Instances**: High-performance virtual machines
- **Global Data Centers**: Multiple regions worldwide
- **Flexible Pricing**: Spot and on-demand instances
- **Enterprise Features**: Security groups, private networks, persistent storage

## Next Steps

- [Installation Guide](./installation) – Install & Configure the SDK
- [Usage Examples](./usage) – Practical SDK Usage Patterns
- [API Reference](./api-reference) – Complete SDK Method Reference
- [Architecture](./architecture) – SDK Design & Structure
- [Troubleshooting](./troubleshooting) – Common Issues and Solutions
