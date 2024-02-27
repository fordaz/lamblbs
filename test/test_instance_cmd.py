from lamblbs.instance_cmd import instance
from click.testing import CliRunner
from unittest.mock import patch
import lamblbs.cmd_utils as utl
import json
import pytest

API_KEY = "abc123"


@patch("lamblbs.cmd_utils.requests.get")
def test_show_all_instance_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": [
            {
                "id": "1",
                "name": "training-node-1",
                "ip": "10.10.10.1",
                "status": "active",
                "ssh_key_names": ["macbook-pro"],
                "file_system_names": ["shared-fs"],
                "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                "instance_type": {
                    "name": "gpu_1x_a100",
                    "description": "1x RTX A100 (24 GB)",
                    "price_cents_per_hour": 110,
                    "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                },
                "hostname": "10-0-8-196.cloud.lambdalabs.com",
                "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                "jupyter_url": "https://...",
            }
        ]
    }

    runner = CliRunner()
    result = runner.invoke(
        instance, ["--json_output", "show-all"], obj={"API_KEY": API_KEY}
    )
    response = json.loads(result.output)
    assert len(response["data"]) == 1
    assert response["data"][0]["id"] == "1"
    assert response["data"][0]["name"] == "training-node-1"


@patch("lamblbs.cmd_utils.requests.get")
def test_types_instance_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "gpu_1x_a100": {
                "instance_type": {
                    "name": "gpu_1x_a100",
                    "description": "1x RTX A100 (24 GB)",
                    "price_cents_per_hour": "80",
                    "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                },
                "regions_with_capacity_available": [
                    {"name": "us-tx-1", "description": "Austin, Texas"}
                ],
            }
        }
    }

    runner = CliRunner()
    result = runner.invoke(
        instance, ["--json_output", "types"], obj={"API_KEY": API_KEY}
    )
    response = json.loads(result.output)
    assert response["data"]["gpu_1x_a100"]["instance_type"]["name"] == "gpu_1x_a100"


@patch("lamblbs.cmd_utils.requests.get")
def test_show_details_instance_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": {
            "id": "1",
            "name": "training-node-1",
            "ip": "10.10.10.1",
            "status": "active",
            "ssh_key_names": ["macbook-pro"],
            "file_system_names": ["shared-fs"],
            "region": {"name": "us-tx-1", "description": "Austin, Texas"},
            "instance_type": {
                "name": "gpu_1x_a100",
                "description": "1x RTX A100 (24 GB)",
                "price_cents_per_hour": 110,
                "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
            },
            "hostname": "10-0-8-196.cloud.lambdalabs.com",
            "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
            "jupyter_url": "https://jupyter...",
        }
    }

    runner = CliRunner()
    result = runner.invoke(
        instance,
        ["--json_output", "show-details", "--id", "1"],
        obj={"API_KEY": API_KEY},
    )
    response = json.loads(result.output)
    assert response["id"] == "1"


@patch("lamblbs.cmd_utils.requests.post")
def test_launch_instance_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "data": [
            {
                "id": "1",
                "name": "training-node-1",
                "ip": "10.10.10.1",
                "status": "active",
                "ssh_key_names": ["macbook-pro"],
                "file_system_names": ["shared-fs"],
                "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                "instance_type": {
                    "name": "gpu_1x_a100",
                    "description": "1x RTX A100 (24 GB)",
                    "price_cents_per_hour": 110,
                    "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                },
                "hostname": "10-0-8-196.cloud.lambdalabs.com",
                "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                "jupyter_url": "https://jupyter...",
            }
        ]
    }

    runner = CliRunner()
    result = runner.invoke(
        instance,
        ["--json_output", "launch", "--ssh_key", "sample-ssh-key"],
        obj={"API_KEY": API_KEY},
    )
    response = json.loads(result.output)
    assert response["data"][0]["id"] == "1"


# TODO implement this unit test
@patch("lamblbs.cmd_utils.requests.get")
def test_check_status_details_instance_success(mock_get):
    pass


# TODO implement this unit test
@patch("lamblbs.cmd_utils.requests.get")
def test_restart_instance_success(mock_get):
    pass


# TODO implement this unit test
@patch("lamblbs.cmd_utils.requests.get")
def test_terminate_instance_success(mock_get):
    pass
