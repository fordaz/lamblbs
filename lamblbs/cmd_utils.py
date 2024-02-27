import click
import requests
import json
import time

LAMBDA_LABS_ENDPOINT = "https://cloud.lambdalabs.com/api/v1"


class APIException(Exception):
    def __init__(self, http_status, body, message, details={}):
        super().__init__(message)
        self.http_status = http_status
        self.body = body
        self.message = message
        self.details = details

    def __str__(self):
        return f"API Exception: {self.message}\nstatus:{self.http_status}\nbody={self.body}\ndetails={self.details}"

    def __repr__(self):
        return f"APIException(http_status={self.http_status}, body={self.body}, details={self.details})"


def do_get(api_name, ctx):
    API_KEY = ctx.obj["API_KEY"]
    url = f"{LAMBDA_LABS_ENDPOINT}/{api_name}"
    headers = {"Authorization": f"Basic {API_KEY}"}
    response = requests.get(url, headers=headers)
    return get_json_or_raise(response, f"Unexpected exception calling {url}")


def do_post(api_name, ctx, payload, is_json=True):
    API_KEY = ctx.obj["API_KEY"]
    url = f"{LAMBDA_LABS_ENDPOINT}/{api_name}"
    headers = {"Authorization": f"Basic {API_KEY}"}
    if is_json:
        response = requests.post(url, headers=headers, json=payload)
    else:
        response = requests.post(url, headers=headers, data=payload)
    return get_json_or_raise(
        response, f"Unexpected exception calling {url}", 200, payload
    )


def do_delete(api_name, ctx):
    API_KEY = ctx.obj["API_KEY"]
    url = f"{LAMBDA_LABS_ENDPOINT}/{api_name}"
    headers = {"Authorization": f"Basic {API_KEY}"}
    response = requests.delete(url, headers=headers)
    return get_json_or_raise(response, f"Unexpected exception calling {url}", 200)


def cli_message(ctx, msg, force=False):
    json_out = ctx.obj["JSON_OUTPUT"]
    if force or not json_out:
        click.echo(msg)


def cli_json_output(data):
    if data:
        print(json.dumps(data))


def enable_http_debug():
    import logging
    import http.client as http_client

    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def save_instance_state(instances_info, state_file, fields=["id", "name", "ip"]):
    infra_state = {"instances": []}
    for info in instances_info["data"]:
        infra_state["instances"].append(info)
    with open(state_file, "w") as state_file:
        state_file.write(json.dumps(infra_state))


def get_instance_details(ctx, id):
    response_json = do_get(f"instances/{id}", ctx)
    return response_json["data"]


def check_instance_status(ctx, id, status):
    max_retries, retry_gap_secs, retry_count = 6, 60, 0
    actual_status = "undefined"
    while retry_count < max_retries:
        instance_details = get_instance_details(ctx, id)
        cli_message(ctx, f"Instance {id} in {instance_details['status']} status")
        if instance_details["status"] == status:
            actual_status = status
            break
        retry_count += 1
        time.sleep(retry_gap_secs)
    cli_message(ctx, f"Instance {id} reached {actual_status} status")


def get_json_or_raise(response, message, expected_http_status=200, details={}):
    if response.status_code != expected_http_status:
        raise APIException(response.status_code, response.text, message, details)
    return response.json()


def get_text_or_raise(response, message, expected_http_status=200, details={}):
    if response.status_code != expected_http_status:
        raise APIException(response.status_code, response.text, message, details)
    return response.text
