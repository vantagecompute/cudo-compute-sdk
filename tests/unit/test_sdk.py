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
"""Unit tests for Cudo Compute SDK."""

from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from cudo_compute_sdk import CudoComputeSDK, get_cudo_compute_sdk


@pytest.fixture
def api_key():
    return "test-api-key-123"


@pytest.fixture
def sdk(api_key):
    return CudoComputeSDK(api_key=api_key)


@pytest.fixture
def mock_response():
    """Create a mock response object."""

    def _create_response(data: Dict[str, Any], status_code: int = 200):
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.is_success = 200 <= status_code < 300
        response.json.return_value = data
        response.raise_for_status = MagicMock()
        if not response.is_success:
            response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Error", request=MagicMock(), response=response
            )
        return response

    return _create_response


class TestSDKInitialization:
    def test_sdk_initialization(self, api_key):
        sdk = CudoComputeSDK(api_key=api_key)
        assert sdk.api_key == api_key
        assert sdk.BASE_URL == "https://rest.compute.cudo.org"
        assert sdk.client.base_url == "https://rest.compute.cudo.org"
        assert sdk.client.headers["Authorization"] == f"Bearer {api_key}"

    @pytest.mark.asyncio
    async def test_sdk_close(self, sdk):
        with patch.object(sdk.client, "aclose", new_callable=AsyncMock) as mock_close:
            await sdk.close()
            mock_close.assert_called_once()

    def test_singleton_get_cudo_compute_sdk(self, api_key):
        sdk1 = get_cudo_compute_sdk(api_key)
        sdk2 = get_cudo_compute_sdk(api_key)
        assert sdk1 is sdk2


class TestVirtualMachines:
    def test_build_create_vm_body_minimal(self, sdk):
        """Test _build_create_vm_body with only required parameters."""
        body = sdk._build_create_vm_body(
            vm_id="test-vm",
            data_center_id="dc-1",
            machine_type="standard",
            boot_disk_image_id="ubuntu-2204",
            vcpus=2,
            memory_gib=4,
            gpus=0,
            boot_disk_size_gib=None,
            password=None,
            ssh_key_source=None,
            custom_ssh_keys=None,
            start_script=None,
            metadata=None,
            security_group_ids=None,
            storage_disk_ids=None,
            commitment_term=None,
            expire_time=None,
            ttl=None,
            nics=None,
            validate_only=False,
        )

        # Check required fields are present
        assert body["vmId"] == "test-vm"
        assert body["dataCenterId"] == "dc-1"
        assert body["machineType"] == "standard"
        assert body["bootDiskImageId"] == "ubuntu-2204"
        assert body["vcpus"] == 2
        assert body["memoryGib"] == 4
        assert body["gpus"] == 0

        # Check optional fields are not present
        assert "bootDiskSizeGib" not in body
        assert "password" not in body
        assert "sshKeySource" not in body
        assert "validateOnly" not in body

    def test_build_create_vm_body_with_all_options(self, sdk):
        """Test _build_create_vm_body with all optional parameters."""
        body = sdk._build_create_vm_body(
            vm_id="test-vm",
            data_center_id="dc-1",
            machine_type="performance",
            boot_disk_image_id="ubuntu-2204",
            vcpus=4,
            memory_gib=8,
            gpus=2,
            boot_disk_size_gib=200,
            password="secure123",
            ssh_key_source="SSH_KEY_SOURCE_USER",
            custom_ssh_keys=["ssh-rsa AAAA..."],
            start_script="#!/bin/bash\necho hello",
            metadata={"env": "prod", "team": "platform"},
            security_group_ids=["sg-1", "sg-2"],
            storage_disk_ids=["disk-1"],
            commitment_term="COMMITMENT_TERM_1_MONTH",
            expire_time="2025-12-31T23:59:59Z",
            ttl="7d",
            nics=None,
            validate_only=True,
        )

        # Check all fields are present
        assert body["bootDiskSizeGib"] == 200
        assert body["password"] == "secure123"
        assert body["sshKeySource"] == "SSH_KEY_SOURCE_USER"
        assert body["customSshKeys"] == ["ssh-rsa AAAA..."]
        assert body["startScript"] == "#!/bin/bash\necho hello"
        assert body["metadata"] == {"env": "prod", "team": "platform"}
        assert body["securityGroupIds"] == ["sg-1", "sg-2"]
        assert body["storageDiskIds"] == ["disk-1"]
        assert body["commitmentTerm"] == "COMMITMENT_TERM_1_MONTH"
        assert body["expireTime"] == "2025-12-31T23:59:59Z"
        assert body["ttl"] == "7d"
        assert body["validateOnly"] is True

    def test_build_create_vm_body_with_nics(self, sdk):
        """Test _build_create_vm_body with NICs (security_group_ids should be ignored)."""
        nics = [
            {
                "assignPublicIp": True,
                "networkId": "net-1",
                "securityGroupIds": ["sg-nic-1"],
            }
        ]
        body = sdk._build_create_vm_body(
            vm_id="test-vm",
            data_center_id="dc-1",
            machine_type="standard",
            boot_disk_image_id="ubuntu-2204",
            vcpus=2,
            memory_gib=4,
            gpus=0,
            boot_disk_size_gib=None,
            password=None,
            ssh_key_source=None,
            custom_ssh_keys=None,
            start_script=None,
            metadata=None,
            security_group_ids=["sg-1", "sg-2"],  # Should be ignored
            storage_disk_ids=None,
            commitment_term=None,
            expire_time=None,
            ttl=None,
            nics=nics,
            validate_only=False,
        )

        # NICs should be present
        assert body["nics"] == nics
        # security_group_ids should NOT be present when nics is provided
        assert "securityGroupIds" not in body

    def test_build_create_vm_body_security_groups_without_nics(self, sdk):
        """Test _build_create_vm_body with security_group_ids and no NICs."""
        body = sdk._build_create_vm_body(
            vm_id="test-vm",
            data_center_id="dc-1",
            machine_type="standard",
            boot_disk_image_id="ubuntu-2204",
            vcpus=2,
            memory_gib=4,
            gpus=0,
            boot_disk_size_gib=None,
            password=None,
            ssh_key_source=None,
            custom_ssh_keys=None,
            start_script=None,
            metadata=None,
            security_group_ids=["sg-1", "sg-2"],
            storage_disk_ids=None,
            commitment_term=None,
            expire_time=None,
            ttl=None,
            nics=None,
            validate_only=False,
        )

        # security_group_ids should be present when nics is None
        assert body["securityGroupIds"] == ["sg-1", "sg-2"]
        assert "nics" not in body

    @pytest.mark.asyncio
    async def test_list_vms(self, sdk, mock_response):
        mock_data = {
            "VMs": [
                {"id": "vm-1", "vcpus": 2, "memory": 4096},
                {"id": "vm-2", "vcpus": 4, "memory": 8192},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            vms = await sdk.list_vms(project_id="project-123")
            assert len(vms) == 2
            assert vms[0].id == "vm-1"
            assert vms[1].vcpus == 4
            mock_get.assert_called_once_with("/v1/projects/project-123/vms", params={})

    @pytest.mark.asyncio
    async def test_list_vms_with_network_filter(self, sdk, mock_response):
        mock_data = {"VMs": [{"id": "vm-1"}]}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            await sdk.list_vms(project_id="project-123", network_id="net-456")
            mock_get.assert_called_once_with(
                "/v1/projects/project-123/vms", params={"networkId": "net-456"}
            )

    @pytest.mark.asyncio
    async def test_get_vm(self, sdk, mock_response):
        mock_data = {"VM": {"id": "vm-1", "vcpus": 2, "state": "ACTIVE"}}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            vm = await sdk.get_vm(project_id="project-123", vm_id="vm-1")
            assert vm.id == "vm-1"
            assert vm.vcpus == 2
            mock_get.assert_called_once_with("/v1/projects/project-123/vms/vm-1")

    @pytest.mark.asyncio
    async def test_create_vm_minimal(self, sdk, mock_response):
        mock_data = {"VM": {"id": "vm-new", "state": "PENDING"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            vm = await sdk.create_vm(
                project_id="project-123",
                vm_id="vm-new",
                data_center_id="dc-1",
                machine_type="standard",
                boot_disk_image_id="ubuntu-2204",
                vcpus=2,
                memory_gib=4,
            )
            assert vm.id == "vm-new"
            call_args = mock_post.call_args
            assert call_args[0][0] == "/v1/projects/project-123/vm"
            json_body = call_args[1]["json"]
            assert json_body["vmId"] == "vm-new"
            assert json_body["vcpus"] == 2

    @pytest.mark.asyncio
    async def test_create_vm_with_options(self, sdk, mock_response):
        mock_data = {"VM": {"id": "vm-new"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            await sdk.create_vm(
                project_id="project-123",
                vm_id="vm-new",
                data_center_id="dc-1",
                machine_type="standard",
                boot_disk_image_id="ubuntu-2204",
                vcpus=4,
                memory_gib=8,
                gpus=1,
                boot_disk_size_gib=200,
                ssh_key_source="SSH_KEY_SOURCE_USER",
                security_group_ids=["sg-1"],
                metadata={"env": "prod"},
                validate_only=True,
            )
            json_body = mock_post.call_args[1]["json"]
            assert json_body["gpus"] == 1
            assert json_body["bootDiskSizeGib"] == 200
            assert json_body["sshKeySource"] == "SSH_KEY_SOURCE_USER"
            assert json_body["securityGroupIds"] == ["sg-1"]
            assert json_body["metadata"] == {"env": "prod"}
            assert json_body["validateOnly"] is True

    @pytest.mark.asyncio
    async def test_terminate_vm(self, sdk, mock_response):
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response({})
            await sdk.terminate_vm(project_id="project-123", vm_id="vm-1")
            mock_post.assert_called_once_with("/v1/projects/project-123/vms/vm-1/terminate")

    @pytest.mark.asyncio
    async def test_start_vm(self, sdk, mock_response):
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response({})
            await sdk.start_vm(project_id="project-123", vm_id="vm-1")
            mock_post.assert_called_once_with("/v1/projects/project-123/vms/vm-1/start")

    @pytest.mark.asyncio
    async def test_stop_vm(self, sdk, mock_response):
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response({})
            await sdk.stop_vm(project_id="project-123", vm_id="vm-1")
            mock_post.assert_called_once_with("/v1/projects/project-123/vms/vm-1/stop")

    @pytest.mark.asyncio
    async def test_reboot_vm(self, sdk, mock_response):
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response({})
            await sdk.reboot_vm(project_id="project-123", vm_id="vm-1")
            mock_post.assert_called_once_with("/v1/projects/project-123/vms/vm-1/reboot")

    @pytest.mark.asyncio
    async def test_resize_vm(self, sdk, mock_response):
        mock_data = {"VM": {"id": "vm-1", "vcpus": 4, "memory": 8192}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            vm = await sdk.resize_vm(project_id="project-123", vm_id="vm-1", vcpus=4, memory_gib=8)
            assert vm.vcpus == 4
            call_args = mock_post.call_args
            params = call_args[1]["params"]
            assert params["vcpus"] == 4
            assert params["memoryGib"] == 8

    @pytest.mark.asyncio
    async def test_connect_vm(self, sdk, mock_response):
        mock_data = {"connectUrl": "https://console.example.com", "token": "abc123"}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            result = await sdk.connect_vm(project_id="project-123", vm_id="vm-1")
            assert result["connectUrl"] == "https://console.example.com"
            assert result["token"] == "abc123"

    @pytest.mark.asyncio
    async def test_monitor_vm(self, sdk, mock_response):
        mock_data = {"cpu": {"usage": 45.5}, "memory": {"usage": 60.2}}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            result = await sdk.monitor_vm(project_id="project-123", vm_id="vm-1")
            assert result["cpu"]["usage"] == 45.5


class TestDataCenters:
    @pytest.mark.asyncio
    async def test_list_vm_data_centers(self, sdk, mock_response):
        mock_data = {
            "dataCenters": [
                {"id": "dc-1", "supplierName": "Cudo"},
                {"id": "dc-2", "supplierName": "Partner"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            dcs = await sdk.list_vm_data_centers()
            assert len(dcs) == 2
            assert dcs[0].id == "dc-1"

    @pytest.mark.asyncio
    async def test_list_vm_machine_types(self, sdk, mock_response):
        mock_data = {
            "machineTypes": [
                {"machineType": "standard", "cpuModel": "Intel Xeon"},
                {"machineType": "performance", "cpuModel": "AMD EPYC"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            mts = await sdk.list_vm_machine_types(project_id="project-123")
            assert len(mts) == 2
            assert mts[0].machine_type == "standard"

    @pytest.mark.asyncio
    async def test_get_vm_machine_type(self, sdk, mock_response):
        # API returns machine type data directly, not wrapped
        mock_data = {"machineType": "standard", "minVcpu": 1.0}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            mt = await sdk.get_vm_machine_type(data_center_id="dc-1", machine_type_id="standard")
            assert mt.machine_type == "standard"


class TestBaremetalMachineTypes:
    @pytest.mark.asyncio
    async def test_list_machine_types(self, sdk, mock_response):
        """Test listing bare-metal machine types returns MachineType objects."""
        mock_data = {
            "machineTypes": [
                {
                    "id": "bm-standard-1",
                    "dataCenterId": "dc-1",
                    "cpuCores": 32,
                    "memoryGib": 128,
                    "cpuModel": "Intel Xeon Gold",
                },
                {
                    "id": "bm-gpu-1",
                    "dataCenterId": "dc-1",
                    "cpuCores": 64,
                    "memoryGib": 256,
                    "gpus": 4,
                    "gpuModelId": "nvidia-a100",
                },
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            machine_types = await sdk.list_machine_types(project_id="project-123")

            # Verify we got MachineType objects
            assert len(machine_types) == 2
            assert machine_types[0].id == "bm-standard-1"
            assert machine_types[0].data_center_id == "dc-1"
            assert machine_types[0].cpu_cores == 32
            assert machine_types[0].memory_gib == 128
            assert machine_types[1].gpus == 4

            # Verify the API was called correctly
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert call_args[0][0] == "/v1/machines-types"
            assert call_args[1]["params"] == {"projectId": "project-123"}

    @pytest.mark.asyncio
    async def test_list_machine_types_no_project(self, sdk, mock_response):
        """Test listing machine types without project ID."""
        mock_data = {"machineTypes": [{"id": "bm-1", "dataCenterId": "dc-1"}]}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            machine_types = await sdk.list_machine_types()

            assert len(machine_types) == 1
            assert machine_types[0].id == "bm-1"

            # Verify no projectId param was passed
            call_args = mock_get.call_args
            assert call_args[1]["params"] == {}

    @pytest.mark.asyncio
    async def test_get_machine_type(self, sdk, mock_response):
        """Test getting a specific bare-metal machine type."""
        mock_data = {
            "machineTypes": [
                {
                    "id": "bm-standard-1",
                    "dataCenterId": "dc-1",
                    "cpuCores": 32,
                    "memoryGib": 128,
                },
                {
                    "id": "bm-standard-2",
                    "dataCenterId": "dc-2",
                    "cpuCores": 64,
                    "memoryGib": 256,
                },
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)

            # Get specific machine type by data center and ID
            mt = await sdk.get_machine_type(data_center_id="dc-1", machine_type_id="bm-standard-1")

            assert mt.id == "bm-standard-1"
            assert mt.data_center_id == "dc-1"
            assert mt.cpu_cores == 32

    @pytest.mark.asyncio
    async def test_get_machine_type_not_found(self, sdk, mock_response):
        """Test getting a machine type that doesn't exist raises error."""
        mock_data = {
            "machineTypes": [
                {"id": "bm-standard-1", "dataCenterId": "dc-1"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)

            # Try to get non-existent machine type
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await sdk.get_machine_type(data_center_id="dc-2", machine_type_id="bm-nonexistent")

            assert "not found" in str(exc_info.value)


class TestImages:
    @pytest.mark.asyncio
    async def test_list_public_vm_images(self, sdk, mock_response):
        mock_data = {
            "images": [
                {"id": "ubuntu-2204", "name": "Ubuntu 22.04"},
                {"id": "debian-12", "name": "Debian 12"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            images = await sdk.list_public_vm_images()
            assert len(images) == 2
            assert images[0].id == "ubuntu-2204"

    @pytest.mark.asyncio
    async def test_list_private_vm_images(self, sdk, mock_response):
        mock_data = {"images": [{"id": "custom-img", "name": "My Image"}]}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            images = await sdk.list_private_vm_images(project_id="project-123")
            assert len(images) == 1

    @pytest.mark.asyncio
    async def test_create_private_vm_image(self, sdk, mock_response):
        mock_data = {"image": {"id": "img-new", "name": "New Image"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            image = await sdk.create_private_vm_image(
                project_id="project-123",
                vm_id="vm-1",
                image_id="img-new",
                description="Test image",
            )
            assert image.id == "img-new"

    @pytest.mark.asyncio
    async def test_delete_private_vm_image(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_private_vm_image(project_id="project-123", image_id="img-1")
            mock_delete.assert_called_once()


class TestDisks:
    @pytest.mark.asyncio
    async def test_list_disks(self, sdk, mock_response):
        mock_data = {
            "disks": [
                {"id": "disk-1", "sizeGib": 100},
                {"id": "disk-2", "sizeGib": 500},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            disks = await sdk.list_disks(project_id="project-123")
            assert len(disks) == 2
            assert disks[0].size_gib == 100

    @pytest.mark.asyncio
    async def test_create_disk(self, sdk, mock_response):
        mock_data = {"disk": {"id": "disk-new", "sizeGib": 100}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            disk = await sdk.create_disk(
                project_id="project-123",
                disk_id="disk-new",
                data_center_id="dc-1",
                size_gib=100,
            )
            assert disk.id == "disk-new"
            assert disk.size_gib == 100

    @pytest.mark.asyncio
    async def test_delete_disk(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_disk(project_id="project-123", disk_id="disk-1")
            mock_delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_attach_disk(self, sdk, mock_response):
        with patch.object(sdk.client, "patch", new_callable=AsyncMock) as mock_patch:
            mock_patch.return_value = mock_response({})
            await sdk.attach_disk(project_id="project-123", disk_id="disk-1", vm_id="vm-1")
            mock_patch.assert_called_once()

    @pytest.mark.asyncio
    async def test_detach_disk(self, sdk, mock_response):
        with patch.object(sdk.client, "put", new_callable=AsyncMock) as mock_put:
            mock_put.return_value = mock_response({})
            await sdk.detach_disk(project_id="project-123", disk_id="disk-1")
            mock_put.assert_called_once()


class TestProjects:
    @pytest.mark.asyncio
    async def test_list_projects(self, sdk, mock_response):
        mock_data = {
            "projects": [
                {"id": "project-1", "billingAccountId": "ba-1"},
                {"id": "project-2", "billingAccountId": "ba-2"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            projects = await sdk.list_projects()
            assert len(projects) == 2
            assert projects[0].id == "project-1"

    @pytest.mark.asyncio
    async def test_get_project(self, sdk, mock_response):
        mock_data = {"id": "project-1", "billingAccountId": "ba-1"}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            project = await sdk.get_project(project_id="project-1")
            assert project.id == "project-1"

    @pytest.mark.asyncio
    async def test_create_project(self, sdk, mock_response):
        mock_data = {"id": "project-new", "billingAccountId": "ba-1"}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            project = await sdk.create_project(
                project_data={"id": "project-new", "billingAccountId": "ba-1"}
            )
            assert project.id == "project-new"

    @pytest.mark.asyncio
    async def test_delete_project(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_project(project_id="project-1")
            mock_delete.assert_called_once()


class TestBillingAccounts:
    @pytest.mark.asyncio
    async def test_list_billing_accounts(self, sdk, mock_response):
        mock_data = {
            "billingAccounts": [
                {"id": "ba-1", "displayName": "Account 1"},
                {"id": "ba-2", "displayName": "Account 2"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            accounts = await sdk.list_billing_accounts()
            assert len(accounts) == 2
            assert accounts[0].id == "ba-1"

    @pytest.mark.asyncio
    async def test_get_billing_account(self, sdk, mock_response):
        # API returns account data directly, not wrapped in billingAccounts array
        mock_data = {"id": "ba-1", "displayName": "Main Account"}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            account = await sdk.get_billing_account(billing_account_id="ba-1")
            assert account.id == "ba-1"
            assert account.display_name == "Main Account"


class TestSSHKeys:
    @pytest.mark.asyncio
    async def test_list_ssh_keys(self, sdk, mock_response):
        mock_data = {
            "sshKeys": [
                {"id": "key-1", "fingerprint": "SHA256:abc"},
                {"id": "key-2", "fingerprint": "SHA256:def"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            keys = await sdk.list_ssh_keys()
            assert len(keys) == 2
            assert keys[0].id == "key-1"

    @pytest.mark.asyncio
    async def test_create_ssh_key(self, sdk, mock_response):
        mock_data = {"sshKey": {"id": "key-new", "publicKey": "ssh-rsa AAAA..."}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            key = await sdk.create_ssh_key(public_key="ssh-rsa AAAA...")
            assert key.id == "key-new"

    @pytest.mark.asyncio
    async def test_delete_ssh_key(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_ssh_key(ssh_key_id="key-1")
            mock_delete.assert_called_once()


class TestSecurityGroups:
    @pytest.mark.asyncio
    async def test_list_security_groups(self, sdk, mock_response):
        mock_data = {
            "securityGroups": [
                {"id": "sg-1", "description": "Web servers"},
                {"id": "sg-2", "description": "Databases"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            sgs = await sdk.list_security_groups(project_id="project-123")
            assert len(sgs) == 2
            assert sgs[0].id == "sg-1"

    @pytest.mark.asyncio
    async def test_create_security_group(self, sdk, mock_response):
        mock_data = {"securityGroup": {"id": "sg-new", "description": "New SG"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            sg = await sdk.create_security_group(
                project_id="project-123",
                security_group_id="sg-new",
                data_center_id="dc-1",
                description="New SG",
            )
            assert sg.id == "sg-new"

    @pytest.mark.asyncio
    async def test_create_security_group_with_rules(self, sdk, mock_response):
        """Test creating security group with rules (tests Dict[str, Any] type annotation fix)."""
        rules = [
            {
                "protocol": "TCP",
                "ports": "80,443",
                "ruleType": "INGRESS",
                "ipRangeCidr": "0.0.0.0/0",
            },
            {
                "protocol": "TCP",
                "ports": "22",
                "ruleType": "INGRESS",
                "ipRangeCidr": "10.0.0.0/8",
            },
        ]
        mock_data = {
            "securityGroup": {
                "id": "sg-with-rules",
                "description": "SG with rules",
                "rules": rules,
            }
        }
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            sg = await sdk.create_security_group(
                project_id="project-123",
                security_group_id="sg-with-rules",
                data_center_id="dc-1",
                description="SG with rules",
                rules=rules,
            )
            assert sg.id == "sg-with-rules"
            assert sg.rules is not None
            assert len(sg.rules) == 2

            # Verify the API was called with rules in the body
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "rules" in call_args[1]["json"]
            assert call_args[1]["json"]["rules"] == rules

    @pytest.mark.asyncio
    async def test_delete_security_group(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_security_group(project_id="project-123", security_group_id="sg-1")
            mock_delete.assert_called_once()


class TestNetworks:
    @pytest.mark.asyncio
    async def test_list_networks(self, sdk, mock_response):
        mock_data = {
            "networks": [
                {"id": "net-1", "ipRange": "10.0.0.0/24"},
                {"id": "net-2", "ipRange": "10.1.0.0/24"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            networks = await sdk.list_networks(project_id="project-123")
            assert len(networks) == 2
            assert networks[0].ip_range == "10.0.0.0/24"

    @pytest.mark.asyncio
    async def test_create_network(self, sdk, mock_response):
        mock_data = {"network": {"id": "net-new", "ipRange": "10.2.0.0/24"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            network = await sdk.create_network(
                project_id="project-123",
                network_id="net-new",
                data_center_id="dc-1",
                ip_range="10.2.0.0/24",
            )
            assert network.id == "net-new"

    @pytest.mark.asyncio
    async def test_delete_network(self, sdk, mock_response):
        with patch.object(sdk.client, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response({})
            await sdk.delete_network(project_id="project-123", network_id="net-1")
            mock_delete.assert_called_once()


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_whoami(self, sdk, mock_response):
        mock_data = {"userId": "user-123", "email": "user@example.com"}
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            result = await sdk.whoami()
            assert result["userId"] == "user-123"
            assert result["email"] == "user@example.com"


class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_http_error_handling(self, sdk, mock_response):
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response({"error": "Not found"}, 404)
            with pytest.raises(httpx.HTTPStatusError):
                await sdk.get_vm(project_id="project-123", vm_id="invalid")

    @pytest.mark.asyncio
    async def test_create_vm_422_error_logging(self, sdk, mock_response):
        """Test that 422 errors are properly logged with response body."""
        error_response = {
            "error": "Validation failed",
            "details": "Invalid machine type",
        }
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(error_response, 422)
            with pytest.raises(httpx.HTTPStatusError):
                await sdk.create_vm(
                    project_id="project-123",
                    vm_id="vm-new",
                    data_center_id="dc-1",
                    machine_type="invalid",
                    boot_disk_image_id="ubuntu-2204",
                    vcpus=2,
                    memory_gib=4,
                )


class TestVolumes:
    @pytest.mark.asyncio
    async def test_list_volumes(self, sdk, mock_response):
        mock_data = {
            "volumes": [
                {"id": "vol-1", "sizeGib": 1000},
                {"id": "vol-2", "sizeGib": 2000},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            result = await sdk.list_volumes(project_id="project-123")
            assert "volumes" in result
            assert len(result["volumes"]) == 2

    @pytest.mark.asyncio
    async def test_create_volume(self, sdk, mock_response):
        mock_data = {"volume": {"id": "vol-new", "sizeGib": 1000}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            result = await sdk.create_volume(
                project_id="project-123",
                volume_id="vol-new",
                data_center_id="dc-1",
                size_gib=1000,
            )
            assert result["volume"]["id"] == "vol-new"


class TestClusters:
    @pytest.mark.asyncio
    async def test_list_clusters(self, sdk, mock_response):
        mock_data = {
            "clusters": [
                {"id": "cluster-1", "state": "RUNNING"},
                {"id": "cluster-2", "state": "STOPPED"},
            ]
        }
        with patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response(mock_data)
            result = await sdk.list_clusters(project_id="project-123")
            assert len(result["clusters"]) == 2

    @pytest.mark.asyncio
    async def test_create_cluster(self, sdk, mock_response):
        mock_data = {"cluster": {"id": "cluster-new", "state": "PENDING"}}
        with patch.object(sdk.client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response(mock_data)
            result = await sdk.create_cluster(
                project_id="project-123",
                cluster_id="cluster-new",
                data_center_id="dc-1",
                machine_type_id="mt-1",
                machine_count=3,
            )
            assert result["cluster"]["id"] == "cluster-new"


class TestSecurityGroupRules:
    @pytest.mark.asyncio
    async def test_create_security_group_rule(self, sdk, mock_response):
        # Mock get_security_group response
        get_sg_data = {
            "securityGroup": {
                "id": "sg-1",
                "rules": [],
            }
        }
        # Mock update_security_group response (returns raw dict, not model)
        update_sg_data = {
            "id": "sg-1",
            "rules": [{"id": "rule-new", "protocol": "TCP", "ports": "22"}],
        }
        with (
            patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get,
            patch.object(sdk.client, "patch", new_callable=AsyncMock) as mock_patch,
        ):
            mock_get.return_value = mock_response(get_sg_data)
            mock_patch.return_value = mock_response(update_sg_data)
            sg = await sdk.create_security_group_rule(
                project_id="project-123",
                security_group_id="sg-1",
                protocol="TCP",
                rule_type="INGRESS",
                ip_range_cidr="0.0.0.0/0",
                ports="22",
            )
            # update_security_group returns a dict, not a SecurityGroup
            assert sg["id"] == "sg-1"
            assert len(sg["rules"]) == 1

    @pytest.mark.asyncio
    async def test_delete_security_group_rule(self, sdk, mock_response):
        # Mock get_security_group response
        get_sg_data = {
            "securityGroup": {
                "id": "sg-1",
                "rules": [{"id": "rule-1", "protocol": "TCP"}],
            }
        }
        # Mock update_security_group response (returns raw dict, not model)
        update_sg_data = {"id": "sg-1", "rules": []}
        with (
            patch.object(sdk.client, "get", new_callable=AsyncMock) as mock_get,
            patch.object(sdk.client, "patch", new_callable=AsyncMock) as mock_patch,
        ):
            mock_get.return_value = mock_response(get_sg_data)
            mock_patch.return_value = mock_response(update_sg_data)
            sg = await sdk.delete_security_group_rule(
                project_id="project-123",
                security_group_id="sg-1",
                rule_id="rule-1",
            )
            # update_security_group returns a dict, not a SecurityGroup
            assert sg["id"] == "sg-1"
