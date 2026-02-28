# Copyright 2025 Vantage Compute Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for Cudo Compute SDK schema models."""

import pytest
from pydantic import ValidationError

from cudo_compute_sdk.schema import (
    VM,
    BillingAccount,
    Cluster,
    ClusterNode,
    DataCenter,
    Disk,
    DiskPoolPricing,
    GpuModel,
    Image,
    InstalledPackage,
    Location,
    Machine,
    MachineType,
    MachineTypePrice,
    MoneyValue,
    Network,
    NetworkPricing,
    Price,
    Project,
    ProjectPermission,
    RechargeSettings,
    SecurityGroup,
    SecurityGroupRule,
    SSHKey,
    VMDataCenter,
    VMMachineType,
    VMMachineTypePrice,
    VMNic,
    VMPrice,
    Volume,
)


class TestPrice:
    def test_price_valid(self):
        price = Price(value="1.23")
        assert price.value == "1.23"

    def test_price_required_field(self):
        with pytest.raises(ValidationError):
            Price()


class TestLocation:
    def test_location_with_coordinates(self):
        location = Location(latitude=51.5074, longitude=-0.1278)
        assert location.latitude == 51.5074
        assert location.longitude == -0.1278

    def test_location_optional_fields(self):
        location = Location()
        assert location.latitude is None
        assert location.longitude is None


class TestInstalledPackage:
    def test_installed_package_full(self):
        package = InstalledPackage(
            name="python3", description="Python 3 interpreter", version="3.12.0"
        )
        assert package.name == "python3"
        assert package.description == "Python 3 interpreter"
        assert package.version == "3.12.0"

    def test_installed_package_minimal(self):
        package = InstalledPackage()
        assert package.name is None
        assert package.description is None
        assert package.version is None


class TestProject:
    def test_project_minimal(self):
        project = Project(id="project-123")
        assert project.id == "project-123"
        assert project.billing_account_id is None

    def test_project_full(self):
        project = Project(
            id="project-123",
            billingAccountId="billing-456",
            resourceCount=5,
            createBy="user@example.com",
        )
        assert project.id == "project-123"
        assert project.billing_account_id == "billing-456"
        assert project.resource_count == 5
        assert project.create_by == "user@example.com"

    def test_project_alias_mapping(self):
        # Test that camelCase aliases map to snake_case attributes
        project = Project(id="test", billingAccountId="ba-123")
        assert project.billing_account_id == "ba-123"


class TestMoneyValue:
    def test_money_value(self):
        money = MoneyValue(value="100.50")
        assert money.value == "100.50"


class TestRechargeSettings:
    def test_recharge_settings_full(self):
        settings = RechargeSettings(
            low=MoneyValue(value="50.00"),
            high=MoneyValue(value="200.00"),
            autoRecharge=True,
            transaction="tx-123",
        )
        assert settings.low.value == "50.00"
        assert settings.high.value == "200.00"
        assert settings.auto_recharge is True
        assert settings.transaction == "tx-123"

    def test_recharge_settings_default(self):
        settings = RechargeSettings()
        assert settings.auto_recharge is False


class TestBillingAccount:
    def test_billing_account_minimal(self):
        account = BillingAccount(id="ba-123")
        assert account.id == "ba-123"

    def test_billing_account_full(self):
        account = BillingAccount(
            id="ba-123",
            createTime="2025-01-01T00:00:00Z",
            displayName="Main Account",
            stripeRef="stripe_123",
            createBy="user@example.com",
            monthlySpend="1000.00",
            hourlySpendRate=MoneyValue(value="1.50"),
            taxId="TAX123",
            invoiceTime="2025-01-31T23:59:59Z",
            billingThreshold=MoneyValue(value="5000.00"),
            monthlySpendLimit=MoneyValue(value="10000.00"),
            hourlySpendLimit=MoneyValue(value="100.00"),
            nextInvoiceTotal="1500.00",
            creditBalance=MoneyValue(value="500.00"),
            creditBalanceRecharge=RechargeSettings(autoRecharge=True),
            billingAddress="123 Main St",
            state="ACTIVE",
            paymentTerms="NET30",
        )
        assert account.id == "ba-123"
        assert account.display_name == "Main Account"
        assert account.monthly_spend == "1000.00"
        assert account.credit_balance.value == "500.00"


class TestProjectPermission:
    def test_project_permission(self):
        perm = ProjectPermission(
            userId="user-123",
            userEmail="user@example.com",
            userPicture="https://example.com/pic.jpg",
            role="OWNER",
            permissionRole="ADMIN",
        )
        assert perm.user_id == "user-123"
        assert perm.user_email == "user@example.com"
        assert perm.role == "OWNER"


class TestSSHKey:
    def test_ssh_key_minimal(self):
        key = SSHKey(id="key-123")
        assert key.id == "key-123"

    def test_ssh_key_full(self):
        key = SSHKey(
            id="key-123",
            createTime="2025-01-01T00:00:00Z",
            publicKey="ssh-rsa AAAAB3...",
            fingerprint="SHA256:abc123",
            type="RSA",
            comment="user@host",
        )
        assert key.id == "key-123"
        assert key.public_key == "ssh-rsa AAAAB3..."
        assert key.fingerprint == "SHA256:abc123"


class TestDisk:
    def test_disk_minimal(self):
        disk = Disk(id="disk-123")
        assert disk.id == "disk-123"

    def test_disk_full(self):
        disk = Disk(
            id="disk-123",
            projectId="project-456",
            dataCenterId="dc-1",
            vmId="vm-789",
            sizeGib=100,
            storageClass="SSD",
            diskType="PERSISTENT",
            publicImageId="ubuntu-2204",
            createTime="2025-01-01T00:00:00Z",
            diskState="READY",
        )
        assert disk.id == "disk-123"
        assert disk.project_id == "project-456"
        assert disk.size_gib == 100
        assert disk.disk_type == "PERSISTENT"


class TestImage:
    def test_image_minimal(self):
        image = Image(id="img-123")
        assert image.id == "img-123"

    def test_image_full(self):
        image = Image(
            id="ubuntu-2204",
            name="Ubuntu 22.04 LTS",
            description="Ubuntu 22.04 LTS Server",
            displayName="Ubuntu 22.04 LTS",
            platform="linux",
            sizeGib=10,
            installedPackages=[
                InstalledPackage(name="python3", version="3.10.12"),
                InstalledPackage(name="docker", version="24.0.0"),
            ],
        )
        assert image.id == "ubuntu-2204"
        assert image.name == "Ubuntu 22.04 LTS"
        assert image.size_gib == 10
        assert len(image.installed_packages) == 2


class TestNetwork:
    def test_network_minimal(self):
        network = Network(id="net-123")
        assert network.id == "net-123"

    def test_network_full(self):
        network = Network(
            id="net-123",
            projectId="project-456",
            dataCenterId="dc-1",
            ipRange="10.0.0.0/24",
            gateway="10.0.0.1",
            priceHr=Price(value="0.01"),
            externalIpAddress="203.0.113.1",
            internalIpAddress="10.0.0.10",
            vmState="RUNNING",
            createTime="2025-01-01T00:00:00Z",
            state="ACTIVE",
        )
        assert network.id == "net-123"
        assert network.ip_range == "10.0.0.0/24"
        assert network.gateway == "10.0.0.1"


class TestSecurityGroupRule:
    def test_security_group_rule(self):
        rule = SecurityGroupRule(
            id="rule-123",
            protocol="TCP",
            ports="22",
            ruleType="INGRESS",
            ipRangeCidr="0.0.0.0/0",
        )
        assert rule.id == "rule-123"
        assert rule.protocol == "TCP"
        assert rule.ports == "22"
        assert rule.rule_type == "INGRESS"


class TestSecurityGroup:
    def test_security_group_minimal(self):
        sg = SecurityGroup(id="sg-123")
        assert sg.id == "sg-123"

    def test_security_group_with_rules(self):
        sg = SecurityGroup(
            id="sg-123",
            projectId="project-456",
            dataCenterId="dc-1",
            description="Web server security group",
            rules=[
                SecurityGroupRule(id="rule-1", protocol="TCP", ports="80", ruleType="INGRESS"),
                SecurityGroupRule(id="rule-2", protocol="TCP", ports="443", ruleType="INGRESS"),
            ],
        )
        assert sg.id == "sg-123"
        assert sg.description == "Web server security group"
        assert len(sg.rules) == 2


class TestGpuModel:
    def test_gpu_model_valid(self):
        gm = GpuModel(
            id="nvidia-a100-pcie",
            vendorName="NVIDIA",
            modelName="A100 80GB PCIe",
            memoryGib=80,
        )
        assert gm.id == "nvidia-a100-pcie"
        assert gm.vendor_name == "NVIDIA"
        assert gm.model_name == "A100 80GB PCIe"
        assert gm.memory_gib == 80

    def test_gpu_model_minimal(self):
        gm = GpuModel(id="test-gpu")
        assert gm.id == "test-gpu"
        assert gm.vendor_name is None
        assert gm.model_name is None
        assert gm.memory_gib is None

    def test_gpu_model_required_id(self):
        with pytest.raises(ValidationError):
            GpuModel()


class TestVMMachineTypePrice:
    def test_vm_machine_type_price(self):
        price = VMMachineTypePrice(
            vcpuPriceHr=Price(value="0.05"),
            memoryGibPriceHr=Price(value="0.01"),
            gpuPriceHr=Price(value="1.50"),
            commitmentTerm="COMMITMENT_TERM_1_MONTH",
        )
        assert price.vcpu_price_hr.value == "0.05"
        assert price.memory_gib_price_hr.value == "0.01"
        assert price.commitment_term == "COMMITMENT_TERM_1_MONTH"


class TestVMMachineType:
    def test_vm_machine_type_minimal(self):
        mt = VMMachineType()
        assert mt.data_center_id is None

    def test_vm_machine_type_full(self):
        mt = VMMachineType(
            dataCenterId="dc-1",
            machineType="standard",
            cpuModel="Intel Xeon",
            gpuModel="NVIDIA A100",
            gpuModelId="a100",
            minVcpuPerMemoryGib=0.25,
            maxVcpuPerMemoryGib=4.0,
            minVcpuPerGpu=1.0,
            maxVcpuPerGpu="Infinity",
            vcpuPriceHr=Price(value="0.05"),
            memoryGibPriceHr=Price(value="0.01"),
            gpuPriceHr=Price(value="1.50"),
            renewableEnergy=True,
            minVcpu=1.0,
            minMemoryGib=1.0,
            prices=[
                VMMachineTypePrice(
                    vcpuPriceHr=Price(value="0.04"), commitmentTerm="COMMITMENT_TERM_1_MONTH"
                )
            ],
        )
        assert mt.data_center_id == "dc-1"
        assert mt.machine_type == "standard"
        assert mt.renewable_energy is True
        assert len(mt.prices) == 1


class TestMachineTypePrice:
    def test_machine_type_price(self):
        price = MachineTypePrice(
            dataCenterId="dc-1",
            machineTypeId="mt-123",
            commitmentTerm="COMMITMENT_TERM_NONE",
            priceHr=Price(value="2.50"),
            ipv4PriceHr=Price(value="0.005"),
        )
        assert price.data_center_id == "dc-1"
        assert price.price_hr.value == "2.50"


class TestMachineType:
    def test_machine_type_minimal(self):
        mt = MachineType(id="mt-123")
        assert mt.id == "mt-123"

    def test_machine_type_full(self):
        mt = MachineType(
            id="mt-123",
            dataCenterId="dc-1",
            architecture="x86_64",
            cpuCores=32,
            cpuSpeedMhz=3400,
            cpuModel="AMD EPYC 7763",
            memoryGib=256,
            disks=2,
            diskSizeGib=1000,
            gpus=4,
            gpuModelId="a100",
            prices=[
                MachineTypePrice(
                    dataCenterId="dc-1",
                    machineTypeId="mt-123",
                    priceHr=Price(value="5.00"),
                )
            ],
            machinesFree=5,
            networkType="10G",
        )
        assert mt.id == "mt-123"
        assert mt.cpu_cores == 32
        assert mt.memory_gib == 256
        assert mt.gpus == 4


class TestMachine:
    def test_machine_minimal(self):
        machine = Machine(id="machine-123")
        assert machine.id == "machine-123"

    def test_machine_full(self):
        machine = Machine(
            id="machine-123",
            dataCenterId="dc-1",
            machineTypeId="mt-123",
            architecture="x86_64",
            cpuCores=32,
            cpuSpeedMhz=3400,
            cpuModel="AMD EPYC",
            memoryGib=256,
            disks=2,
            diskSizeGib=1000,
            gpus=4,
            gpuModelId="a100",
            state="ACTIVE",
            powerState="ON",
            os="ubuntu-2204",
            hostname="machine-123.example.com",
            externalIpAddresses=["203.0.113.1"],
            projectId="project-456",
            createTime="2025-01-01T00:00:00Z",
            createBy="user@example.com",
            commitmentTerm="COMMITMENT_TERM_1_MONTH",
            priceHr=Price(value="5.00"),
            sshKeySource="SSH_KEY_SOURCE_USER",
        )
        assert machine.id == "machine-123"
        assert machine.cpu_cores == 32
        assert machine.hostname == "machine-123.example.com"


class TestVMNic:
    def test_vm_nic(self):
        nic = VMNic(
            networkId="net-123",
            externalIpAddress="203.0.113.1",
            internalIpAddress="10.0.0.10",
            networkAddress="10.0.0.0/24",
            securityGroupIds=["sg-1", "sg-2"],
        )
        assert nic.network_id == "net-123"
        assert nic.external_ip_address == "203.0.113.1"
        assert len(nic.security_group_ids) == 2


class TestVMPrice:
    def test_vm_price(self):
        price = VMPrice(
            vcpuPriceHr=Price(value="0.05"),
            totalVcpuPriceHr=Price(value="0.10"),
            memoryGibPriceHr=Price(value="0.01"),
            totalMemoryPriceHr=Price(value="0.04"),
            totalPriceHr=Price(value="0.14"),
        )
        assert price.vcpu_price_hr.value == "0.05"
        assert price.total_price_hr.value == "0.14"


class TestVM:
    def test_vm_minimal(self):
        vm = VM(id="vm-123")
        assert vm.id == "vm-123"

    def test_vm_full(self):
        vm = VM(
            id="vm-123",
            datacenterId="dc-1",
            machineType="standard",
            externalIpAddress="203.0.113.1",
            internalIpAddress="10.0.0.10",
            publicIpAddress="203.0.113.1",
            memory=4096,
            cpuModel="Intel Xeon",
            vcpus=2,
            gpuModel="NVIDIA A100",
            gpuModelId="a100",
            gpuQuantity=1,
            bootDiskSizeGib=100,
            renewableEnergy=True,
            imageId="ubuntu-2204",
            publicImageId="ubuntu-2204",
            publicImageName="Ubuntu 22.04 LTS",
            createBy="user@example.com",
            nics=[
                VMNic(networkId="net-123", internalIpAddress="10.0.0.10"),
            ],
            securityGroupIds=["sg-1"],
            shortState="RUNNING",
            bootDisk=Disk(id="disk-boot", sizeGib=100),
            storageDisks=[Disk(id="disk-1", sizeGib=500)],
            metadata={"env": "production"},
            state="ACTIVE",
            createTime="2025-01-01T00:00:00Z",
            price=VMPrice(totalPriceHr=Price(value="1.50")),
            commitmentTerm="COMMITMENT_TERM_NONE",
            sshKeySource="SSH_KEY_SOURCE_USER",
            projectId="project-456",
        )
        assert vm.id == "vm-123"
        assert vm.vcpus == 2
        assert vm.memory == 4096
        assert vm.gpu_quantity == 1
        assert len(vm.nics) == 1
        assert len(vm.storage_disks) == 1


class TestDiskPoolPricing:
    def test_disk_pool_pricing(self):
        pricing = DiskPoolPricing(storageClass="SSD", diskGibPriceHr=Price(value="0.0001"))
        assert pricing.storage_class == "SSD"
        assert pricing.disk_gib_price_hr.value == "0.0001"


class TestNetworkPricing:
    def test_network_pricing(self):
        pricing = NetworkPricing(priceHr=Price(value="0.01"))
        assert pricing.price_hr.value == "0.01"


class TestVMDataCenter:
    def test_vm_data_center_minimal(self):
        dc = VMDataCenter(id="dc-1")
        assert dc.id == "dc-1"

    def test_vm_data_center_full(self):
        dc = VMDataCenter(
            id="gb-bournemouth-1",
            supplierName="Cudo Compute",
            renewableEnergy=True,
            diskPoolPricing=[
                DiskPoolPricing(storageClass="SSD", diskGibPriceHr=Price(value="0.0001"))
            ],
            networkPricing=[NetworkPricing(priceHr=Price(value="0.01"))],
            networkPriceHr=Price(value="0.01"),
            ipv4PriceHr=Price(value="0.005"),
            ipv4Free=1,
            s3Endpoint="https://s3.example.com",
            location=Location(latitude=50.7192, longitude=-1.8808),
            objectStorageGibPriceHr=Price(value="0.00005"),
        )
        assert dc.id == "gb-bournemouth-1"
        assert dc.renewable_energy is True
        assert dc.ipv4_free == 1
        assert len(dc.disk_pool_pricing) == 1


class TestDataCenter:
    def test_data_center_minimal(self):
        dc = DataCenter(id="dc-1")
        assert dc.id == "dc-1"

    def test_data_center_full(self):
        dc = DataCenter(
            id="dc-1",
            name="Bournemouth",
            country="United Kingdom",
            region="Europe",
            location=Location(latitude=50.7192, longitude=-1.8808),
        )
        assert dc.id == "dc-1"
        assert dc.name == "Bournemouth"
        assert dc.country == "United Kingdom"


class TestVolume:
    def test_volume_minimal(self):
        volume = Volume(id="vol-123")
        assert volume.id == "vol-123"

    def test_volume_full(self):
        volume = Volume(
            id="vol-123",
            projectId="project-456",
            dataCenterId="dc-1",
            sizeGib=1000,
            state="READY",
            createTime="2025-01-01T00:00:00Z",
            priceHr=Price(value="0.10"),
            mountPoint="/mnt/volume",
        )
        assert volume.id == "vol-123"
        assert volume.size_gib == 1000
        assert volume.mount_point == "/mnt/volume"


class TestClusterNode:
    def test_cluster_node(self):
        node = ClusterNode(id="node-1", vmId="vm-123", role="worker", state="ACTIVE")
        assert node.id == "node-1"
        assert node.vm_id == "vm-123"
        assert node.role == "worker"


class TestCluster:
    def test_cluster_minimal(self):
        cluster = Cluster(id="cluster-123")
        assert cluster.id == "cluster-123"

    def test_cluster_full(self):
        cluster = Cluster(
            id="cluster-123",
            projectId="project-456",
            dataCenterId="dc-1",
            clusterType="KUBERNETES",
            state="RUNNING",
            createTime="2025-01-01T00:00:00Z",
            nodes=[
                ClusterNode(id="node-1", vmId="vm-1", role="master"),
                ClusterNode(id="node-2", vmId="vm-2", role="worker"),
            ],
            metadata={"version": "1.28"},
        )
        assert cluster.id == "cluster-123"
        assert cluster.cluster_type == "KUBERNETES"
        assert len(cluster.nodes) == 2


class TestAliasMapping:
    """Test that camelCase API responses map correctly to snake_case Python attributes."""

    def test_project_alias_mapping(self):
        data = {"id": "p-1", "billingAccountId": "ba-1", "resourceCount": 5}
        project = Project(**data)
        assert project.billing_account_id == "ba-1"
        assert project.resource_count == 5

    def test_vm_alias_mapping(self):
        data = {
            "id": "vm-1",
            "datacenterId": "dc-1",
            "machineType": "standard",
            "bootDiskSizeGib": 100,
            "createTime": "2025-01-01T00:00:00Z",
        }
        vm = VM(**data)
        assert vm.datacenter_id == "dc-1"
        assert vm.machine_type == "standard"
        assert vm.boot_disk_size_gib == 100

    def test_billing_account_alias_mapping(self):
        data = {
            "id": "ba-1",
            "displayName": "Main",
            "monthlySpend": "1000",
            "creditBalance": {"value": "500"},
        }
        account = BillingAccount(**data)
        assert account.display_name == "Main"
        assert account.monthly_spend == "1000"
        assert account.credit_balance.value == "500"
