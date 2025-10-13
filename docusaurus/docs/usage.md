---
title: Usage Examples
description: Practical examples of using the Cudo Compute SDK
---

# Usage Examples

This guide provides practical examples of common operations using the Cudo Compute SDK.

## Basic Setup

All examples assume you've initialized the SDK:

```python
import asyncio
from cudo_compute_sdk import CudoComputeSDK

async def main():
    sdk = CudoComputeSDK(api_key="your-api-key")
    
    try:
        # Your code here
        pass
    finally:
        await sdk.close()

asyncio.run(main())
```

## Project Management

### List All Projects

```python
projects = await sdk.list_projects()
for project in projects:
    print(f"Project: {project.id}")
```

### Get Project Details

```python
project = await sdk.get_project(project_id="my-project")
print(f"Project: {project.id}")
print(f"Resources: {project.resource_count}")
```

### Create a New Project

```python
project = await sdk.create_project(
    project_id="ml-training-project",
    billing_account_id="billing-account-123"
)
```

## Virtual Machine Management

### List VMs in a Project

```python
vms = await sdk.list_vms(project_id="my-project")
for vm in vms:
    print(f"VM: {vm.id}")
    print(f"  Status: {vm.state}")
    print(f"  vCPUs: {vm.vcpus}, Memory: {vm.memory_gib}GB")
    print(f"  GPUs: {vm.gpus}")
```

### Get VM Details

```python
vm = await sdk.get_vm(
    project_id="my-project",
    vm_id="my-vm-001"
)
print(f"VM State: {vm.state}")
print(f"Public IP: {vm.public_ip_address}")
```

### Create a New VM

```python
vm = await sdk.create_vm(
    project_id="my-project",
    vm_id="gpu-training-vm",
    data_center_id="gb-bournemouth-1",
    machine_type="standard",
    boot_disk_image_id="ubuntu-2204-lts",
    vcpus=8,
    memory_gib=32,
    gpus=1,
    boot_disk_size_gib=100,
    ssh_key_source="SSH_KEY_SOURCE_USER",
    metadata={"purpose": "ml-training"}
)
print(f"Created VM: {vm.id}")
```

### Start a VM

```python
await sdk.start_vm(
    project_id="my-project",
    vm_id="my-vm-001"
)
```

### Stop a VM

```python
await sdk.stop_vm(
    project_id="my-project",
    vm_id="my-vm-001"
)
```

### Restart a VM

```python
await sdk.restart_vm(
    project_id="my-project",
    vm_id="my-vm-001"
)
```

### Delete a VM

```python
await sdk.terminate_vm(
    project_id="my-project",
    vm_id="my-vm-001"
)
```

## Data Center & Machine Type Discovery

### List Available Data Centers

```python
data_centers = await sdk.list_data_centers()
for dc in data_centers:
    print(f"Data Center: {dc.id}")
    print(f"  Region: {dc.region_name}")
    print(f"  Country: {dc.country_code}")
```

### Get Available Machine Types for a Data Center

```python
machine_types = await sdk.list_machine_types_for_data_center(
    data_center_id="gb-bournemouth-1"
)
for mt in machine_types:
    print(f"Machine Type: {mt.machine_type}")
    print(f"  vCPUs: {mt.vcpus}, Memory: {mt.memory_gib}GB")
    print(f"  GPUs: {mt.gpu_model if mt.gpu_model else 'None'}")
```

### List Available VM Images

```python
images = await sdk.list_images()
for image in images:
    print(f"Image: {image.id}")
    print(f"  OS: {image.os_name} {image.os_version}")
```

## Network Management

### List Networks

```python
networks = await sdk.list_networks(project_id="my-project")
for network in networks:
    print(f"Network: {network.id}")
```

### Create a Network

```python
network = await sdk.create_network(
    project_id="my-project",
    network_id="ml-cluster-network"
)
```

### Delete a Network

```python
await sdk.delete_network(
    project_id="my-project",
    network_id="ml-cluster-network"
)
```

## Security Groups

### List Security Groups

```python
security_groups = await sdk.list_security_groups(project_id="my-project")
for sg in security_groups:
    print(f"Security Group: {sg.id}")
```

### Create Security Group with Rules

```python
# First create the security group
sg = await sdk.create_security_group(
    project_id="my-project",
    security_group_id="web-server-sg"
)

# Add rules
await sdk.create_security_group_rule(
    project_id="my-project",
    security_group_id="web-server-sg",
    rule_id="allow-http",
    direction="RULE_DIRECTION_INGRESS",
    protocol="tcp",
    ports="80",
    source="0.0.0.0/0"
)

await sdk.create_security_group_rule(
    project_id="my-project",
    security_group_id="web-server-sg",
    rule_id="allow-https",
    direction="RULE_DIRECTION_INGRESS",
    protocol="tcp",
    ports="443",
    source="0.0.0.0/0"
)

await sdk.create_security_group_rule(
    project_id="my-project",
    security_group_id="web-server-sg",
    rule_id="allow-ssh",
    direction="RULE_DIRECTION_INGRESS",
    protocol="tcp",
    ports="22",
    source="0.0.0.0/0"
)
```

## SSH Key Management

### List SSH Keys

```python
ssh_keys = await sdk.list_ssh_keys(project_id="my-project")
for key in ssh_keys:
    print(f"SSH Key: {key.id}")
```

### Add SSH Key

```python
with open("~/.ssh/id_rsa.pub") as f:
    public_key = f.read()

ssh_key = await sdk.create_ssh_key(
    project_id="my-project",
    ssh_key_id="my-workstation-key",
    public_key=public_key
)
```

### Delete SSH Key

```python
await sdk.delete_ssh_key(
    project_id="my-project",
    ssh_key_id="my-workstation-key"
)
```

## Storage Management

### List Disks

```python
disks = await sdk.list_disks(project_id="my-project")
for disk in disks:
    print(f"Disk: {disk.id}")
    print(f"  Size: {disk.size_gib}GB")
```

### Create a Disk

```python
disk = await sdk.create_disk(
    project_id="my-project",
    disk_id="data-disk-01",
    data_center_id="gb-bournemouth-1",
    storage_class="network",
    size_gib=500
)
```

### Attach Disk to VM

```python
await sdk.attach_disk_to_vm(
    project_id="my-project",
    vm_id="my-vm-001",
    disk_id="data-disk-01"
)
```

### Detach Disk from VM

```python
await sdk.detach_disk_from_vm(
    project_id="my-project",
    vm_id="my-vm-001",
    disk_id="data-disk-01"
)
```

## Complete Example: ML Training Environment

Here's a complete example that sets up an ML training environment:

```python
import asyncio
from cudo_compute_sdk import CudoComputeSDK

async def setup_ml_environment():
    sdk = CudoComputeSDK(api_key="your-api-key")
    
    try:
        project_id = "ml-training-project"
        
        # 1. Create network
        print("Creating network...")
        network = await sdk.create_network(
            project_id=project_id,
            network_id="ml-network"
        )
        
        # 2. Create security group
        print("Creating security group...")
        sg = await sdk.create_security_group(
            project_id=project_id,
            security_group_id="ml-sg"
        )
        
        # Allow SSH
        await sdk.create_security_group_rule(
            project_id=project_id,
            security_group_id="ml-sg",
            rule_id="allow-ssh",
            direction="RULE_DIRECTION_INGRESS",
            protocol="tcp",
            ports="22",
            source="0.0.0.0/0"
        )
        
        # Allow Jupyter
        await sdk.create_security_group_rule(
            project_id=project_id,
            security_group_id="ml-sg",
            rule_id="allow-jupyter",
            direction="RULE_DIRECTION_INGRESS",
            protocol="tcp",
            ports="8888",
            source="0.0.0.0/0"
        )
        
        # 3. Create storage disk
        print("Creating storage disk...")
        disk = await sdk.create_disk(
            project_id=project_id,
            disk_id="ml-data-disk",
            data_center_id="gb-bournemouth-1",
            storage_class="network",
            size_gib=1000
        )
        
        # 4. Create GPU VM
        print("Creating GPU VM...")
        vm = await sdk.create_vm(
            project_id=project_id,
            vm_id="ml-training-gpu",
            data_center_id="gb-bournemouth-1",
            machine_type="gpu",
            boot_disk_image_id="ubuntu-2204-lts-cuda",
            vcpus=16,
            memory_gib=64,
            gpus=1,
            boot_disk_size_gib=200,
            ssh_key_source="SSH_KEY_SOURCE_USER",
            security_group_ids=["ml-sg"],
            storage_disk_ids=["ml-data-disk"],
            start_script="""#!/bin/bash
                apt-get update
                apt-get install -y python3-pip
                pip3 install jupyter torch torchvision
                jupyter notebook --ip=0.0.0.0 --allow-root
            """
        )
        
        print(f"✓ ML environment created!")
        print(f"  VM ID: {vm.id}")
        print(f"  Public IP: {vm.public_ip_address}")
        print(f"  Access Jupyter at: http://{vm.public_ip_address}:8888")
        
    finally:
        await sdk.close()

asyncio.run(setup_ml_environment())
```

## Best Practices

### 1. Always Close the SDK

Use try/finally or async context managers:

```python
async def main():
    sdk = CudoComputeSDK(api_key="...")
    try:
        # your code
        pass
    finally:
        await sdk.close()
```

### 2. Handle Errors Gracefully

```python
from httpx import HTTPStatusError

try:
    vm = await sdk.get_vm(project_id="...", vm_id="...")
except HTTPStatusError as e:
    if e.response.status_code == 404:
        print("VM not found")
    else:
        raise
```

### 3. Use Environment Variables for API Keys

Never hardcode API keys in your source code.

### 4. Implement Retry Logic for Long Operations

```python
import asyncio

async def wait_for_vm_running(sdk, project_id, vm_id, timeout=300):
    start = asyncio.get_event_loop().time()
    while True:
        vm = await sdk.get_vm(project_id, vm_id)
        if vm.state == "RUNNING":
            return vm
        if asyncio.get_event_loop().time() - start > timeout:
            raise TimeoutError("VM did not start in time")
        await asyncio.sleep(5)
```

## Next Steps

- [API Reference](./api-reference) – Complete SDK method documentation
- [Architecture](./architecture) – SDK design and internals
- [Troubleshooting](./troubleshooting) – Common issues and solutions

