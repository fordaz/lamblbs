import click
import uuid
from . import cmd_utils as utl


@click.group()
@click.pass_context
@click.option("--json_output", is_flag=True, default=False)
def instance(ctx, json_output):
    ctx.obj["JSON_OUTPUT"] = json_output


@click.command()
@click.pass_context
def types(ctx):
    utl.cli_message(ctx, "List instance types")
    instance_types = utl.do_get("instance-types", ctx)
    utl.cli_json_output(instance_types)


@click.command()
@click.pass_context
@click.option(
    "--state_file", default=None, help="Name of the file to persist instances info"
)
def show_all(ctx, state_file):
    utl.cli_message(ctx, "List running instances")
    all_instances = utl.do_get("instances", ctx)
    utl.cli_json_output(all_instances)
    if state_file:
        utl.save_instance_state(all_instances, state_file)


@click.command()
@click.pass_context
@click.option("--id", required=True, help="Id of the instance to check the status for")
def show_details(ctx, id):
    utl.cli_message(ctx, f"Show details for instance {id}")
    instance_details = utl.get_instance_details(ctx, id)
    utl.cli_json_output(instance_details)


@click.command()
@click.pass_context
@click.option("--id", default=None, help="Id of the instance to check the status for")
@click.option("--status", default="active", help="Name of the status to wait for")
def check_status(ctx, id, status):
    if id:
        utl.check_instance_status(ctx, id, status)
    else:
        all_instances = utl.do_get("instances", ctx)
        if not all_instances["data"]:
            utl.cli_message(ctx, "No instances available", force=True)
            return
        ids = list(map(lambda info: info["id"], all_instances["data"]))
        for id in ids:
            utl.check_instance_status(ctx, id, status)


@click.command()
@click.option("--name", default=None, help="Name of the new instance")
@click.option("--type", default="gpu_1x_a10", help="Instance Type")
@click.option("--region", default="us-east-1", help="Region")
@click.option("--ssh_key", required=True, help="SSH Key to access the instance")
@click.option("--qty", default=1, help="Number of instances")
@click.option(
    "--fs_name", default=None, help="A file system name to be attached to the instance"
)
@click.pass_context
def launch(ctx, name, type, region, ssh_key, qty, fs_name):
    payload = {
        "region_name": region,
        "instance_type_name": type,
        "ssh_key_names": [ssh_key],
        "quantity": qty,
        "name": name if name else str(uuid.uuid4()),
    }
    if fs_name:
        payload["file_system_names"] = [fs_name]

    utl.cli_message(ctx, f"Launch instance with parameters {payload}")

    launched_instance = utl.do_post("instance-operations/launch", ctx, payload)
    utl.cli_json_output(launched_instance)


@click.command()
@click.option(
    "--instance_id",
    required=True,
    help="Instance id to terminate",
)
@click.pass_context
# TODO change to support a list of ids
def terminate(ctx, instance_id):
    utl.cli_message(ctx, f"Terminate instance {instance_id}")
    payload = {"instance_ids": [instance_id]}
    terminated_instance = utl.do_post("instance-operations/terminate", ctx, payload)
    utl.cli_json_output(terminated_instance)


@click.command()
@click.option(
    "--instance_id",
    required=True,
    help="Instance id to terminate",
)
@click.pass_context
def restart(ctx, instance_id):
    utl.cli_message(f"Restarting instance {instance_id}")
    payload = {"instance_ids": [instance_id]}
    response = utl.do_post("instance-operations/restart", ctx, payload)
    restarted_instance = utl.get_json_or_raise(
        response, "Unable to restart instance {instance_id}"
    )
    utl.cli_json_output(restarted_instance)


instance.add_command(types)
instance.add_command(show_all)
instance.add_command(show_details)
instance.add_command(check_status)
instance.add_command(launch)
instance.add_command(terminate)
instance.add_command(restart)
