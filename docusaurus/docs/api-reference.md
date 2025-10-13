---
title: API Reference
description: Complete SDK method reference
---

# API Reference

Complete reference for all methods in the Cudo Compute SDK.

## CudoComputeSDK

The main SDK class for interacting with Cudo Compute.

### Initialization

```python
from cudo_compute_sdk import CudoComputeSDK

sdk = CudoComputeSDK(api_key: str)
```

**Parameters:**
- `api_key` (str): Your Cudo Compute API key

### Resource Management

#### `async close()`

Close the HTTP client and cleanup resources.

```python
await sdk.close()
```

Always call this when done with the SDK, or use try/finally pattern.

---

## Projects

### `async list_projects() -> List[Project]`

List all projects in your account.

**Returns:** List of `Project` objects

**Example:**
```python
projects = await sdk.list_projects()
for project in projects:
    print(f"Project: {project.id}")
```

### `async get_project(project_id: str) -> Project`

Get details of a specific project.

**Parameters:**
- `project_id` (str): Project ID

**Returns:** `Project` object

### `async create_project(project_id: str, billing_account_id: Optional[str] = None) -> Project`

Create a new project.

**Parameters:**
- `project_id` (str): Unique project identifier
- `billing_account_id` (Optional[str]): Billing account to associate

**Returns:** Created `Project` object

### `async delete_project(project_id: str) -> None`

Delete a project.

**Parameters:**
- `project_id` (str): Project ID to delete

---

## Virtual Machines

### `async list_vms(project_id: str, network_id: Optional[str] = None) -> List[VM]`

List all virtual machines in a project.

**Parameters:**
- `project_id` (str): Project ID
- `network_id` (Optional[str]): Filter by network ID

**Returns:** List of `VM` objects

### `async get_vm(project_id: str, vm_id: str) -> VM`

Get details of a specific virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID

**Returns:** `VM` object with current state and configuration

### `async create_vm(...) -> VM`

Create and start a new virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): Unique VM identifier
- `data_center_id` (str): Data center ID (e.g., "gb-bournemouth-1")
- `machine_type` (str): Machine type ("standard", "performance", "gpu")
- `boot_disk_image_id` (str): Boot disk image ID
- `vcpus` (int): Number of vCPUs
- `memory_gib` (int): Memory in GiB
- `gpus` (int): Number of GPUs (default: 0)
- `boot_disk_size_gib` (Optional[int]): Boot disk size in GiB
- `password` (Optional[str]): Root/admin password
- `ssh_key_source` (Optional[str]): SSH key source
- `custom_ssh_keys` (Optional[List[str]]): Custom SSH public keys
- `start_script` (Optional[str]): Startup script/cloud-init
- `metadata` (Optional[Dict[str, str]]): VM metadata
- `security_group_ids` (Optional[List[str]]): Security group IDs
- `storage_disk_ids` (Optional[List[str]]): Storage disk IDs
- `commitment_term` (Optional[str]): Commitment term
- `expire_time` (Optional[str]): Expiration time
- `ttl` (Optional[str]): Time to live
- `nics` (Optional[List[Dict[str, Any]]]): Network interface configs
- `validate_only` (bool): Only validate without creating

**Returns:** Created `VM` object

**Example:**
```python
vm = await sdk.create_vm(
    project_id="my-project",
    vm_id="my-vm-001",
    data_center_id="gb-bournemouth-1",
    machine_type="standard",
    boot_disk_image_id="ubuntu-2204-lts",
    vcpus=4,
    memory_gib=8,
    ssh_key_source="SSH_KEY_SOURCE_USER"
)
```

### `async start_vm(project_id: str, vm_id: str) -> VM`

Start a stopped virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID

**Returns:** Updated `VM` object

### `async stop_vm(project_id: str, vm_id: str) -> VM`

Stop a running virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID

**Returns:** Updated `VM` object

### `async restart_vm(project_id: str, vm_id: str) -> VM`

Restart a virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID

**Returns:** Updated `VM` object

### `async terminate_vm(project_id: str, vm_id: str) -> None`

Permanently delete a virtual machine.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID

---

## Data Centers

### `async list_data_centers() -> List[DataCenter]`

List all available data centers.

**Returns:** List of `DataCenter` objects

**Example:**
```python
data_centers = await sdk.list_data_centers()
for dc in data_centers:
    print(f"{dc.id}: {dc.region_name}, {dc.country_code}")
```

### `async get_data_center(data_center_id: str) -> DataCenter`

Get details of a specific data center.

**Parameters:**
- `data_center_id` (str): Data center ID

**Returns:** `DataCenter` object

### `async list_machine_types_for_data_center(data_center_id: str) -> List[VMMachineType]`

List available machine types for a data center.

**Parameters:**
- `data_center_id` (str): Data center ID

**Returns:** List of `VMMachineType` objects

---

## Images

### `async list_images() -> List[Image]`

List all available VM images.

**Returns:** List of `Image` objects

**Example:**
```python
images = await sdk.list_images()
for image in images:
    print(f"{image.id}: {image.os_name} {image.os_version}")
```

---

## Networks

### `async list_networks(project_id: str) -> List[Network]`

List all networks in a project.

**Parameters:**
- `project_id` (str): Project ID

**Returns:** List of `Network` objects

### `async create_network(project_id: str, network_id: str) -> Network`

Create a new network.

**Parameters:**
- `project_id` (str): Project ID
- `network_id` (str): Network ID

**Returns:** Created `Network` object

### `async delete_network(project_id: str, network_id: str) -> None`

Delete a network.

**Parameters:**
- `project_id` (str): Project ID
- `network_id` (str): Network ID

---

## Security Groups

### `async list_security_groups(project_id: str) -> List[SecurityGroup]`

List all security groups in a project.

**Parameters:**
- `project_id` (str): Project ID

**Returns:** List of `SecurityGroup` objects

### `async create_security_group(project_id: str, security_group_id: str) -> SecurityGroup`

Create a new security group.

**Parameters:**
- `project_id` (str): Project ID
- `security_group_id` (str): Security group ID

**Returns:** Created `SecurityGroup` object

### `async create_security_group_rule(...) -> SecurityGroupRule`

Add a rule to a security group.

**Parameters:**
- `project_id` (str): Project ID
- `security_group_id` (str): Security group ID
- `rule_id` (str): Rule ID
- `direction` (str): "RULE_DIRECTION_INGRESS" or "RULE_DIRECTION_EGRESS"
- `protocol` (str): "tcp", "udp", or "icmp"
- `ports` (Optional[str]): Port or port range (e.g., "80", "8000-9000")
- `source` (Optional[str]): Source CIDR (e.g., "0.0.0.0/0")
- `destination` (Optional[str]): Destination CIDR

**Returns:** Created `SecurityGroupRule` object

**Example:**
```python
rule = await sdk.create_security_group_rule(
    project_id="my-project",
    security_group_id="web-sg",
    rule_id="allow-http",
    direction="RULE_DIRECTION_INGRESS",
    protocol="tcp",
    ports="80",
    source="0.0.0.0/0"
)
```

### `async delete_security_group(project_id: str, security_group_id: str) -> None`

Delete a security group.

**Parameters:**
- `project_id` (str): Project ID
- `security_group_id` (str): Security group ID

---

## SSH Keys

### `async list_ssh_keys(project_id: str) -> List[SSHKey]`

List all SSH keys in a project.

**Parameters:**
- `project_id` (str): Project ID

**Returns:** List of `SSHKey` objects

### `async create_ssh_key(project_id: str, ssh_key_id: str, public_key: str) -> SSHKey`

Add an SSH key to a project.

**Parameters:**
- `project_id` (str): Project ID
- `ssh_key_id` (str): SSH key ID
- `public_key` (str): SSH public key content

**Returns:** Created `SSHKey` object

**Example:**
```python
ssh_key = await sdk.create_ssh_key(
    project_id="my-project",
    ssh_key_id="my-key",
    public_key="ssh-rsa AAAAB3NzaC1yc2E..."
)
```

### `async delete_ssh_key(project_id: str, ssh_key_id: str) -> None`

Delete an SSH key.

**Parameters:**
- `project_id` (str): Project ID
- `ssh_key_id` (str): SSH key ID

---

## Storage / Disks

### `async list_disks(project_id: str) -> List[Disk]`

List all disks in a project.

**Parameters:**
- `project_id` (str): Project ID

**Returns:** List of `Disk` objects

### `async create_disk(...) -> Disk`

Create a new disk.

**Parameters:**
- `project_id` (str): Project ID
- `disk_id` (str): Disk ID
- `data_center_id` (str): Data center ID
- `storage_class` (str): Storage class ("network" or "local")
- `size_gib` (int): Disk size in GiB

**Returns:** Created `Disk` object

**Example:**
```python
disk = await sdk.create_disk(
    project_id="my-project",
    disk_id="data-disk",
    data_center_id="gb-bournemouth-1",
    storage_class="network",
    size_gib=500
)
```

### `async attach_disk_to_vm(project_id: str, vm_id: str, disk_id: str) -> None`

Attach a disk to a VM.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID
- `disk_id` (str): Disk ID

### `async detach_disk_from_vm(project_id: str, vm_id: str, disk_id: str) -> None`

Detach a disk from a VM.

**Parameters:**
- `project_id` (str): Project ID
- `vm_id` (str): VM ID
- `disk_id` (str): Disk ID

### `async delete_disk(project_id: str, disk_id: str) -> None`

Delete a disk.

**Parameters:**
- `project_id` (str): Project ID
- `disk_id` (str): Disk ID

---

## Data Models

All API responses are returned as Pydantic models with full type safety.

### Key Models

- **Project**: Project information
- **VM**: Virtual machine details
- **DataCenter**: Data center information
- **VMMachineType**: Available machine configurations
- **Image**: OS images for VMs
- **Network**: Virtual network
- **SecurityGroup**: Firewall rules container
- **SecurityGroupRule**: Individual firewall rule
- **SSHKey**: SSH public key
- **Disk**: Storage disk

See the [schema.py](https://github.com/vantagecompute/cudo-compute-sdk/blob/main/cudo_compute_sdk/schema.py) file for complete model definitions.

---

## Error Handling

The SDK raises `httpx.HTTPStatusError` for API errors:

```python
from httpx import HTTPStatusError

try:
    vm = await sdk.get_vm(project_id="...", vm_id="...")
except HTTPStatusError as e:
    print(f"Status: {e.response.status_code}")
    print(f"Error: {e.response.json()}")
```

Common status codes:
- `401`: Authentication failed (invalid API key)
- `403`: Permission denied
- `404`: Resource not found
- `422`: Invalid request parameters
- `429`: Rate limit exceeded
- `500`: Server error

---

## Type Hints

The SDK includes comprehensive type hints for IDE support:

```python
from cudo_compute_sdk import CudoComputeSDK
from cudo_compute_sdk.schema import VM, Project

async def example(sdk: CudoComputeSDK) -> VM:
    projects: list[Project] = await sdk.list_projects()
    vms: list[VM] = await sdk.list_vms(project_id=projects[0].id)
    return vms[0]
```
