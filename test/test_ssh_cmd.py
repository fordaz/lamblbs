from lamblbs.ssh_cmd import ssh
from click.testing import CliRunner
from unittest.mock import patch
import lamblbs.cmd_utils as utl
import json

API_KEY = "abc123"


@patch("lamblbs.cmd_utils.requests.get")
def test_list_ssh_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "data": [
            {"id": "1", "name": "ssh-key-1", "public_key": "ssh-rsa AAAA001"},
            {"id": "2", "name": "ssh-key-2", "public_key": "ssh-rsa AAAAB02"},
        ]
    }

    runner = CliRunner()
    result = runner.invoke(ssh, ["--json_output", "list"], obj={"API_KEY": API_KEY})

    response = json.loads(result.output)
    assert len(response["data"]) == 2


@patch("lamblbs.cmd_utils.requests.get")
def test_list_ssh_fails(mock_get):
    mock_get.return_value.status_code = 401

    runner = CliRunner()
    result = runner.invoke(ssh, ["--json_output", "list"], obj={"API_KEY": API_KEY})
    assert 1 == result.exit_code
    assert isinstance(result.exception, utl.APIException)
    assert result.exception.http_status == 401


@patch("lamblbs.cmd_utils.requests.post")
def test_add_ssh_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "data": {
            "id": "1",
            "name": "my-ssh-key",
            "public_key": "ssh-rsa AAAAB001",
            "private_key": "-----BEGIN RSA PRIVATE KEY-----\nKEY CONTENT-----END RSA PRIVATE KEY-----\n",
        }
    }

    runner = CliRunner()
    result = runner.invoke(
        ssh, ["--json_output", "add", "--name", "my-ssh-key"], obj={"API_KEY": API_KEY}
    )

    response = json.loads(result.output)
    assert response["data"]["id"] == "1"
    assert response["data"]["name"] == "my-ssh-key"


@patch("lamblbs.cmd_utils.requests.post")
def test_add_ssh_missing_name(mock_post):
    mock_post.return_value.status_code = 200

    runner = CliRunner()
    result = runner.invoke(ssh, ["--json_output", "add"], obj={"API_KEY": API_KEY})
    assert 2 == result.exit_code
    assert "Missing option '--name'" in result.output


@patch("lamblbs.cmd_utils.requests.delete")
def test_delete_ssh_success(mock_delete):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"data": {}}

    runner = CliRunner()
    result = runner.invoke(
        ssh, ["--json_output", "delete", "--id", "1"], obj={"API_KEY": API_KEY}
    )

    response = json.loads(result.output)
    assert response["data"] is not None
