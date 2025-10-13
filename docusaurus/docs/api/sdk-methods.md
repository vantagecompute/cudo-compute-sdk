---
title: SDK API Documentation
description: Auto-generated API documentation from SDK docstrings
---

# SDK API Documentation

This documentation is auto-generated from the SDK source code docstrings.

## CudoComputeSDK

SDK for interacting with the Cudo Compute REST API.

This SDK provides methods to manage virtual machines, data centers,
machine types, images, networks, and other cloud resources on Cudo Compute.

Authentication is done via bearer token (API key).

API Base URL: https://rest.compute.cudo.org

### Projects

#### `list_projects(self, page_token: Optional[str] = None, page_size: Optional[int] = None) -> List[cudo_compute_sdk.schema.Project]`

List projects accessible by the current user.

**Parameters:**

- page_token: Page token for pagination
- page_size: Results per page

**Returns:**

List of Project model instances

---

#### `get_project(self, project_id: str) -> cudo_compute_sdk.schema.Project`

Get details of a specific project.

**Parameters:**

- project_id: Project ID

**Returns:**

Project model instance

---

#### `create_project(self, project_data: Dict[str, Any]) -> cudo_compute_sdk.schema.Project`

Create a new project.

**Parameters:**

- project_data: Project configuration

**Returns:**

Created Project model instance

---

#### `delete_project(self, project_id: str) -> None`

Delete a project.

**Parameters:**

- project_id: Project ID to delete

**Returns:**

None

---

### Virtual Machines

#### `list_vms(self, project_id: str, network_id: Optional[str] = None) -> List[cudo_compute_sdk.schema.VM]`

List all virtual machines in a project.

**Parameters:**

- project_id: Project ID to list VMs from
- network_id: Optional network ID to filter VMs

**Returns:**

List of VM model instances

---

#### `get_vm(self, project_id: str, vm_id: str) -> cudo_compute_sdk.schema.VM`

Get details of a specific virtual machine.

**Parameters:**

- project_id: Project ID
- vm_id: Virtual machine ID

**Returns:**

VM model instance with pricing information

---

#### `create_vm(self, project_id: str, vm_id: str, data_center_id: str, machine_type: str, boot_disk_image_id: str, vcpus: int, memory_gib: int, gpus: int = 0, boot_disk_size_gib: Optional[int] = None, password: Optional[str] = None, ssh_key_source: Optional[str] = None, custom_ssh_keys: Optional[List[str]] = None, start_script: Optional[str] = None, metadata: Optional[Dict[str, str]] = None, security_group_ids: Optional[List[str]] = None, storage_disk_ids: Optional[List[str]] = None, commitment_term: Optional[str] = None, expire_time: Optional[str] = None, ttl: Optional[str] = None, nics: Optional[List[Dict[str, Any]]] = None, validate_only: bool = False) -> cudo_compute_sdk.schema.VM`

Create and start a new virtual machine.

**Parameters:**

- project_id: Project ID to create VM in
- vm_id: Unique identifier for the VM
- data_center_id: Data center to create VM in
- machine_type: Machine type to use (e.g., 'standard', 'performance')
- boot_disk_image_id: Boot disk image ID (public or private image)
- vcpus: Number of vCPUs (must meet machine type requirements)
- memory_gib: Memory in GiB (must meet machine type requirements)
- gpus: Number of GPUs (default: 0)
- boot_disk_size_gib: Boot disk size in GiB (if not set, uses image default)
- password: Root/admin password (for Windows VMs or custom Linux setup)
- ssh_key_source: SSH key source - 'SSH_KEY_SOURCE_PROJECT', 'SSH_KEY_SOURCE_USER', or 'SSH_KEY_SOURCE_NONE'
- custom_ssh_keys: List of custom SSH public keys to add
- start_script: Startup script/cloud-init to run on first boot
- metadata: VM metadata key-value pairs
- security_group_ids: List of security group IDs (ignored if nics provided)
- storage_disk_ids: List of storage disk IDs to attach
- commitment_term: Commitment term ('COMMITMENT_TERM_NONE', 'COMMITMENT_TERM_1_MONTH', etc.)
- expire_time: Expiration time in ISO 8601 format
- ttl: Time to live duration string
- nics: List of network interface configurations with assignPublicIp, networkId, securityGroupIds
- validate_only: Only validate request without creating (default: False)

**Returns:**

Created VM model instance

**Example:**

```python
>>> vm = await sdk.create_vm(
...     project_id="my-project",
...     vm_id="my-vm-001",
...     data_center_id="gb-bournemouth-1",
...     machine_type="standard",
...     boot_disk_image_id="ubuntu-2204-lts",
...     vcpus=2,
...     memory_gib=4,
...     gpus=0,
...     ssh_key_source="SSH_KEY_SOURCE_USER"
... )
```

---

#### `start_vm(self, project_id: str, vm_id: str) -> None`

Start a stopped virtual machine.

**Parameters:**

- project_id: Project ID
- vm_id: Virtual machine ID

**Returns:**

None

---

#### `stop_vm(self, project_id: str, vm_id: str) -> None`

Stop a running virtual machine. The VM can be started again later.

**Parameters:**

- project_id: Project ID
- vm_id: Virtual machine ID

**Returns:**

None

---

#### `terminate_vm(self, project_id: str, vm_id: str) -> None`

Permanently delete a virtual machine. All data on the VM's boot disk will be lost. Attached storage disks will be detached but not deleted.

**Parameters:**

- project_id: Project ID
- vm_id: Virtual machine ID to delete

**Returns:**

None

---

### Data Centers

#### `get_data_center(self, data_center_id: str) -> cudo_compute_sdk.schema.VMDataCenter`

Get details of a specific data center. Note: This is a helper method that filters list_vm_data_centers results.

**Parameters:**

- data_center_id: Data center ID

**Returns:**

VMDataCenter model instance

---

### Images

### Networks

#### `list_networks(self, project_id: str, page_number: Optional[int] = None, page_size: Optional[int] = None) -> List[cudo_compute_sdk.schema.Network]`

List all virtual networks in a project.

**Parameters:**

- project_id: Project ID
- page_number: Page number for pagination
- page_size: Results per page

**Returns:**

List of Network model instances

---

#### `create_network(self, project_id: str, network_id: str, data_center_id: str, ip_range: str) -> cudo_compute_sdk.schema.Network`

Create a new virtual network.

**Parameters:**

- project_id: Project ID
- network_id: Unique network ID
- data_center_id: Data center ID
- ip_range: IP range for the network (CIDR notation)

**Returns:**

Created Network model instance

---

#### `delete_network(self, project_id: str, network_id: str) -> None`

Delete a virtual network.

**Parameters:**

- project_id: Project ID
- network_id: Network ID to delete

**Returns:**

None

---

### Security Groups

#### `list_security_groups(self, project_id: str, data_center_id: Optional[str] = None, page_number: Optional[int] = None, page_size: Optional[int] = None) -> List[cudo_compute_sdk.schema.SecurityGroup]`

List security groups in a project.

**Parameters:**

- project_id: Project ID
- data_center_id: Optional data center filter
- page_number: Page number for pagination
- page_size: Results per page

**Returns:**

List of SecurityGroup model instances

---

#### `create_security_group(self, project_id: str, security_group_id: str, data_center_id: str, description: Optional[str] = None, rules: Optional[List[Dict[str, Any]]] = None) -> cudo_compute_sdk.schema.SecurityGroup`

Create a new security group.

**Parameters:**

- project_id: Project ID
- security_group_id: Unique security group identifier
- data_center_id: Data center ID where the security group will be created
- description: Optional security group description
- rules: Optional list of security rules

**Returns:**

Created SecurityGroup model instance

---

#### `create_security_group_rule(self, project_id: str, security_group_id: str, protocol: str, rule_type: str, ip_range_cidr: str, ports: Optional[str] = None, icmp_type: Optional[str] = None) -> cudo_compute_sdk.schema.SecurityGroup`

Create a new rule in a security group.

**Parameters:**

- project_id: Project ID
- security_group_id: Security group ID
- protocol: Protocol (PROTOCOL_TCP, PROTOCOL_UDP, PROTOCOL_ICMP, etc.)
- rule_type: Rule type (RULE_TYPE_INBOUND, RULE_TYPE_OUTBOUND)
- ip_range_cidr: IP range in CIDR format
- ports: Port range (e.g., "80", "80-443")
- icmp_type: ICMP type (for ICMP protocol)

**Returns:**

Updated SecurityGroup with new rule

---

#### `delete_security_group(self, project_id: str, security_group_id: str) -> None`

Delete a security group.

**Parameters:**

- project_id: Project ID
- security_group_id: Security group ID to delete

**Returns:**

None

---

### SSH Keys

#### `list_ssh_keys(self, page_number: Optional[int] = None, page_size: Optional[int] = None) -> List[cudo_compute_sdk.schema.SSHKey]`

List SSH keys of the current user.

**Parameters:**

- page_number: Page number for pagination
- page_size: Results per page

**Returns:**

List of SSHKey model instances

---

#### `create_ssh_key(self, public_key: str) -> cudo_compute_sdk.schema.SSHKey`

Create an SSH key for accessing machines.

**Parameters:**

- public_key: SSH public key

**Returns:**

Created SSHKey model instance

---

#### `delete_ssh_key(self, ssh_key_id: str) -> None`

Delete an SSH key.

**Parameters:**

- ssh_key_id: SSH key ID to delete

**Returns:**

None

---

### Storage

#### `list_disks(self, project_id: str, page_number: Optional[int] = None, page_size: Optional[int] = None, data_center_id: Optional[str] = None) -> List[cudo_compute_sdk.schema.Disk]`

List disks in a project.

**Parameters:**

- project_id: Project ID
- page_number: Page number for pagination
- page_size: Results per page
- data_center_id: Optional data center filter

**Returns:**

List of Disk model instances

---

#### `create_disk(self, project_id: str, disk_id: str, data_center_id: str, size_gib: int, disk_type: Optional[str] = None) -> cudo_compute_sdk.schema.Disk`

Create a new virtual machine disk.

**Parameters:**

- project_id: Project ID
- disk_id: Unique disk ID
- data_center_id: Data center ID
- size_gib: Disk size in GiB
- disk_type: Optional disk type

**Returns:**

Created Disk model instance

---

#### `delete_disk(self, project_id: str, disk_id: str) -> None`

Delete a virtual machine disk. The disk must be detached from any VMs first.

**Parameters:**

- project_id: Project ID
- disk_id: Disk ID to delete

**Returns:**

None

---
