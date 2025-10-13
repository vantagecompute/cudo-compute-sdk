---
title: Contributing
description: How to contribute to Cudo Compute SDK development
---

# Contributing

Short guide for contributing to the Cudo Compute SDK.

## Environment Setup

```bash
git clone https://github.com/vantagecompute/cudo-compute-sdk.git
cd cudo-compute-sdk
pip install uv
uv sync
```

Run tests:

```bash
just unit
```

## Project Structure

```text
cudo_compute_sdk/
    __init__.py    # Main CudoComputeSDK class
    schema.py      # Pydantic models for API types
```

## Documentation

Generate API documentation:

```bash
just docs-generate-api
```

Build documentation:

```bash
just docs-build
```

## Adding SDK Methods

When adding new methods to the SDK:

1. Add the method to `CudoComputeSDK` class in `__init__.py`
2. Include comprehensive docstrings with:
   - Method description
   - Args section with type information
   - Returns section
   - Example usage
3. Add or update Pydantic models in `schema.py` if needed
4. Run `just docs-generate-api` to update documentation

Example:

```python
async def create_vm(
    self,
    project_id: str,
    vm_id: str,
    data_center_id: str,
    machine_type: str,
    boot_disk_image_id: str,
    vcpus: int,
    memory_gib: int,
    gpus: int = 0,
) -> VM:
    """Create a new virtual machine.
    
    Args:
        project_id: Project ID to create VM in
        vm_id: Unique identifier for the VM
        data_center_id: Data center ID
        machine_type: Machine type (e.g., 'standard', 'gpu')
        boot_disk_image_id: Boot disk image ID
        vcpus: Number of vCPUs
        memory_gib: Memory in GiB
        gpus: Number of GPUs (default: 0)
    
    Returns:
        Created VM model instance
        
    Example:
        >>> vm = await sdk.create_vm(
        ...     project_id="my-project",
        ...     vm_id="my-vm",
        ...     data_center_id="gb-bournemouth-1",
        ...     machine_type="standard",
        ...     boot_disk_image_id="ubuntu-2204-lts",
        ...     vcpus=4,
        ...     memory_gib=8
        ... )
    """
    # Implementation here
```

## Standards

- Python 3.12+
- Type hints required for all functions
- Async/await for all network operations
- Comprehensive docstrings following Google style
- Pydantic models for all API responses

## Testing

```bash
just lint        # Check code style
just typecheck   # Run static type checker
just unit        # Run unit tests
just integration # Run integration tests (if available)
```

Write focused tests for each new method (happy path + error cases).

## Code Quality

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions focused and single-purpose
- Handle errors appropriately with clear error messages
- Never expose API keys in logs or error messages

## Documentation

After making changes:

1. Update docstrings in code
2. Regenerate API docs: `just docs-generate-api`
3. Update usage examples in `docs/usage.md` if needed
4. Test documentation build: `just docs-build`

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Run linting and type checking
6. Ensure all tests pass
7. Update documentation
8. Submit a pull request with clear description

**PR Description Should Include:**
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes

## Release Process (Maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build and test documentation
5. Create git tag
6. Build package: `uv build`
7. Publish to PyPI: `uv publish`
8. Create GitHub release

## Communication

- **Questions**: Use [GitHub Discussions](https://github.com/vantagecompute/cudo-compute-sdk/discussions)
- **Bugs**: Open [GitHub Issues](https://github.com/vantagecompute/cudo-compute-sdk/issues)
- **Security**: Email security@vantagecompute.ai

When reporting issues, include:
- SDK version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (with API keys removed)

---

Thank you for contributing to Cudo Compute SDK!
