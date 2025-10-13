---
title: Data Models
description: Schema and data model documentation
---

# Data Models

Pydantic models used for API requests and responses.

## BillingAccount

Cudo Compute billing account.

**Fields:**

- `id`: <class 'str'>
- `create_time`: typing.Optional[str]
- `display_name`: typing.Optional[str]
- `stripe_ref`: typing.Optional[str]
- `create_by`: typing.Optional[str]
- `monthly_spend`: typing.Optional[str]
- `hourly_spend_rate`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `tax_id`: typing.Optional[str]
- `invoice_time`: typing.Optional[str]
- `billing_threshold`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `monthly_spend_limit`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `hourly_spend_limit`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `next_invoice_total`: typing.Optional[str]
- `credit_balance`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `credit_balance_recharge`: typing.Optional[cudo_compute_sdk.schema.RechargeSettings]
- `billing_address`: typing.Optional[str]
- `state`: typing.Optional[str]
- `payment_terms`: typing.Optional[str]
- `delete_time`: typing.Optional[str]
- `purge_time`: typing.Optional[str]

---

## Cluster

Compute cluster.

**Fields:**

- `id`: <class 'str'>
- `project_id`: typing.Optional[str]
- `data_center_id`: typing.Optional[str]
- `cluster_type`: typing.Optional[str]
- `state`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `nodes`: typing.Optional[typing.List[cudo_compute_sdk.schema.ClusterNode]]
- `metadata`: typing.Optional[typing.Dict[str, typing.Any]]

---

## ClusterNode

Cluster node.

**Fields:**

- `id`: typing.Optional[str]
- `vm_id`: typing.Optional[str]
- `role`: typing.Optional[str]
- `state`: typing.Optional[str]

---

## DataCenter

Generic data center (for bare-metal or other services).

**Fields:**

- `id`: <class 'str'>
- `name`: typing.Optional[str]
- `country`: typing.Optional[str]
- `region`: typing.Optional[str]
- `location`: typing.Optional[cudo_compute_sdk.schema.Location]

---

## Disk

Storage disk.

**Fields:**

- `id`: <class 'str'>
- `project_id`: typing.Optional[str]
- `data_center_id`: typing.Optional[str]
- `vm_id`: typing.Optional[str]
- `size_gib`: typing.Optional[int]
- `storage_class`: typing.Optional[str]
- `disk_type`: typing.Optional[str]
- `public_image_id`: typing.Optional[str]
- `private_image_id`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `disk_state`: typing.Optional[str]

---

## DiskPoolPricing

Data center disk pool pricing.

**Fields:**

- `storage_class`: typing.Optional[str]
- `disk_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]

---

## Image

VM or machine image.

**Fields:**

- `id`: <class 'str'>
- `name`: typing.Optional[str]
- `description`: typing.Optional[str]
- `display_name`: typing.Optional[str]
- `platform`: typing.Optional[str]
- `size_gib`: typing.Optional[int]
- `installed_packages`: typing.Optional[typing.List[cudo_compute_sdk.schema.InstalledPackage]]

---

## InstalledPackage

Installed package information.

**Fields:**

- `name`: typing.Optional[str]
- `description`: typing.Optional[str]
- `version`: typing.Optional[str]

---

## Location

Geographic location.

**Fields:**

- `latitude`: typing.Optional[float]
- `longitude`: typing.Optional[float]

---

## Machine

Bare-metal machine instance.

**Fields:**

- `data_center_id`: typing.Optional[str]
- `id`: <class 'str'>
- `machine_type_id`: typing.Optional[str]
- `architecture`: typing.Optional[str]
- `cpu_cores`: typing.Optional[int]
- `cpu_speed_mhz`: typing.Optional[int]
- `cpu_model`: typing.Optional[str]
- `memory_gib`: typing.Optional[int]
- `disks`: typing.Optional[int]
- `disk_size_gib`: typing.Optional[int]
- `gpus`: typing.Optional[int]
- `gpu_model_id`: typing.Optional[str]
- `state`: typing.Optional[str]
- `power_state`: typing.Optional[str]
- `os`: typing.Optional[str]
- `hostname`: typing.Optional[str]
- `external_ip_addresses`: typing.Optional[typing.List[str]]
- `project_id`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `create_by`: typing.Optional[str]
- `commitment_term`: typing.Optional[str]
- `price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `user_data`: typing.Optional[str]
- `ssh_key_source`: typing.Optional[str]
- `custom_ssh_keys`: typing.Optional[typing.List[str]]
- `start_script`: typing.Optional[str]

---

## MachineType

Bare-metal machine type.

**Fields:**

- `data_center_id`: typing.Optional[str]
- `id`: <class 'str'>
- `architecture`: typing.Optional[str]
- `cpu_cores`: typing.Optional[int]
- `cpu_speed_mhz`: typing.Optional[int]
- `cpu_model`: typing.Optional[str]
- `memory_gib`: typing.Optional[int]
- `disks`: typing.Optional[int]
- `disk_size_gib`: typing.Optional[int]
- `gpus`: typing.Optional[int]
- `gpu_model_id`: typing.Optional[str]
- `prices`: typing.Optional[typing.List[cudo_compute_sdk.schema.MachineTypePrice]]
- `machines_free`: typing.Optional[int]
- `network_type`: typing.Optional[str]

---

## MachineTypePrice

Bare-metal machine type pricing.

**Fields:**

- `data_center_id`: typing.Optional[str]
- `machine_type_id`: typing.Optional[str]
- `commitment_term`: typing.Optional[str]
- `price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `ipv4_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]

---

## MoneyValue

Money/currency value.

**Fields:**

- `value`: <class 'str'>

---

## Network

Virtual network.

**Fields:**

- `project_id`: typing.Optional[str]
- `id`: <class 'str'>
- `data_center_id`: typing.Optional[str]
- `ip_range`: typing.Optional[str]
- `gateway`: typing.Optional[str]
- `price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `external_ip_address`: typing.Optional[str]
- `internal_ip_address`: typing.Optional[str]
- `vm_state`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `state`: typing.Optional[str]

---

## NetworkPricing

Data center network pricing.

**Fields:**

- `price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]

---

## Price

Price value.

**Fields:**

- `value`: <class 'str'>

---

## Project

Cudo Compute project.

**Fields:**

- `id`: <class 'str'>
- `billing_account_id`: typing.Optional[str]
- `resource_count`: typing.Optional[int]
- `create_by`: typing.Optional[str]

---

## ProjectPermission

Project user permission.

**Fields:**

- `user_id`: typing.Optional[str]
- `user_email`: typing.Optional[str]
- `user_picture`: typing.Optional[str]
- `role`: typing.Optional[str]
- `permission_role`: typing.Optional[str]

---

## RechargeSettings

Auto-recharge settings for billing account.

**Fields:**

- `low`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `high`: typing.Optional[cudo_compute_sdk.schema.MoneyValue]
- `auto_recharge`: <class 'bool'>
- `transaction`: typing.Optional[str]

---

## SSHKey

SSH key.

**Fields:**

- `id`: <class 'str'>
- `create_time`: typing.Optional[str]
- `public_key`: typing.Optional[str]
- `fingerprint`: typing.Optional[str]
- `type`: typing.Optional[str]
- `comment`: typing.Optional[str]

---

## SecurityGroup

Security group.

**Fields:**

- `project_id`: typing.Optional[str]
- `data_center_id`: typing.Optional[str]
- `id`: <class 'str'>
- `description`: typing.Optional[str]
- `rules`: typing.Optional[typing.List[cudo_compute_sdk.schema.SecurityGroupRule]]

---

## SecurityGroupRule

Security group rule.

**Fields:**

- `id`: typing.Optional[str]
- `protocol`: typing.Optional[str]
- `ports`: typing.Optional[str]
- `rule_type`: typing.Optional[str]
- `ip_range_cidr`: typing.Optional[str]
- `icmp_type`: typing.Optional[str]

---

## VM

Virtual machine instance.

**Fields:**

- `datacenter_id`: typing.Optional[str]
- `machine_type`: typing.Optional[str]
- `id`: <class 'str'>
- `external_ip_address`: typing.Optional[str]
- `internal_ip_address`: typing.Optional[str]
- `public_ip_address`: typing.Optional[str]
- `memory`: typing.Optional[int]
- `cpu_model`: typing.Optional[str]
- `vcpus`: typing.Optional[int]
- `gpu_model`: typing.Optional[str]
- `gpu_model_id`: typing.Optional[str]
- `gpu_quantity`: typing.Optional[int]
- `boot_disk_size_gib`: typing.Optional[int]
- `renewable_energy`: typing.Optional[bool]
- `image_id`: typing.Optional[str]
- `public_image_id`: typing.Optional[str]
- `public_image_name`: typing.Optional[str]
- `private_image_id`: typing.Optional[str]
- `image_name`: typing.Optional[str]
- `create_by`: typing.Optional[str]
- `nics`: typing.Optional[typing.List[cudo_compute_sdk.schema.VMNic]]
- `rules`: typing.Optional[typing.List[cudo_compute_sdk.schema.SecurityGroupRule]]
- `security_group_ids`: typing.Optional[typing.List[str]]
- `short_state`: typing.Optional[str]
- `boot_disk`: typing.Optional[cudo_compute_sdk.schema.Disk]
- `storage_disks`: typing.Optional[typing.List[cudo_compute_sdk.schema.Disk]]
- `metadata`: typing.Optional[typing.Dict[str, typing.Any]]
- `state`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `expire_time`: typing.Optional[str]
- `price`: typing.Optional[cudo_compute_sdk.schema.VMPrice]
- `commitment_term`: typing.Optional[str]
- `commitment_end_time`: typing.Optional[str]
- `ssh_key_source`: typing.Optional[str]
- `authorized_ssh_keys`: typing.Optional[str]
- `security_groups`: typing.Optional[typing.List[cudo_compute_sdk.schema.SecurityGroup]]
- `project_id`: typing.Optional[str]

---

## VMDataCenter

VM data center.

**Fields:**

- `id`: <class 'str'>
- `supplier_name`: typing.Optional[str]
- `renewable_energy`: typing.Optional[bool]
- `disk_pool_pricing`: typing.Optional[typing.List[cudo_compute_sdk.schema.DiskPoolPricing]]
- `network_pricing`: typing.Optional[typing.List[cudo_compute_sdk.schema.NetworkPricing]]
- `network_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `ipv4_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `ipv4_free`: typing.Optional[int]
- `s3_endpoint`: typing.Optional[str]
- `location`: typing.Optional[cudo_compute_sdk.schema.Location]
- `object_storage_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]

---

## VMMachineType

VM machine type configuration and pricing.

**Fields:**

- `data_center_id`: typing.Optional[str]
- `machine_type`: typing.Optional[str]
- `cpu_model`: typing.Optional[str]
- `gpu_model`: typing.Optional[str]
- `gpu_model_id`: typing.Optional[str]
- `min_vcpu_per_memory_gib`: typing.Optional[float]
- `max_vcpu_per_memory_gib`: typing.Optional[float]
- `min_vcpu_per_gpu`: typing.Optional[float]
- `max_vcpu_per_gpu`: typing.Optional[typing.Any]
- `vcpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `memory_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `gpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `min_storage_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `ipv4_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `renewable_energy`: typing.Optional[bool]
- `max_vcpu_free`: typing.Optional[int]
- `total_vcpu_free`: typing.Optional[int]
- `max_memory_gib_free`: typing.Optional[int]
- `total_memory_gib_free`: typing.Optional[int]
- `max_gpu_free`: typing.Optional[int]
- `total_gpu_free`: typing.Optional[int]
- `max_storage_gib_free`: typing.Optional[int]
- `total_storage_gib_free`: typing.Optional[int]
- `min_vcpu`: typing.Optional[float]
- `min_memory_gib`: typing.Optional[float]
- `prices`: typing.Optional[typing.List[cudo_compute_sdk.schema.VMMachineTypePrice]]

---

## VMMachineTypePrice

VM machine type pricing for commitment terms.

**Fields:**

- `vcpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `memory_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `gpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `commitment_term`: typing.Optional[str]

---

## VMNic

VM network interface.

**Fields:**

- `network_id`: typing.Optional[str]
- `external_ip_address`: typing.Optional[str]
- `internal_ip_address`: typing.Optional[str]
- `network_address`: typing.Optional[str]
- `security_group_ids`: typing.Optional[typing.List[str]]

---

## VMPrice

VM pricing breakdown.

**Fields:**

- `vcpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `total_vcpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `memory_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `total_memory_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `gpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `total_gpu_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `storage_gib_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `total_storage_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `ipv4_address_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `total_price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]

---

## Volume

NFS volume.

**Fields:**

- `id`: <class 'str'>
- `project_id`: typing.Optional[str]
- `data_center_id`: typing.Optional[str]
- `size_gib`: typing.Optional[int]
- `state`: typing.Optional[str]
- `create_time`: typing.Optional[str]
- `price_hr`: typing.Optional[cudo_compute_sdk.schema.Price]
- `mount_point`: typing.Optional[str]

---
