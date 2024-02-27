from lamblbs.fs_cmd import fs
from click.testing import CliRunner
from unittest.mock import patch
import lamblbs.cmd_utils as utl
import json

API_KEY = "abc123"


@patch("lamblbs.cmd_utils.requests.get")
def test_list_fs_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": []}

    runner = CliRunner()
    result = runner.invoke(fs, ["--json_output", "list"], obj={"API_KEY": API_KEY})

    response = json.loads(result.output)
    assert len(response["data"]) == 0


@patch("lamblbs.cmd_utils.requests.get")
def test_list_fs_fails(mock_get):
    mock_get.return_value.status_code = 401

    runner = CliRunner()
    result = runner.invoke(fs, ["--json_output", "list"], obj={"API_KEY": API_KEY})
    assert 1 == result.exit_code
    assert isinstance(result.exception, utl.APIException)
    assert result.exception.http_status == 401
