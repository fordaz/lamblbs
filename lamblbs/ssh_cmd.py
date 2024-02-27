import click
from . import cmd_utils as utl


@click.group()
@click.pass_context
@click.option("--json_output", is_flag=True, default=False)
def ssh(ctx, json_output):
    ctx.obj["JSON_OUTPUT"] = json_output


@click.command()
@click.pass_context
def list(ctx):
    utl.cli_message(ctx, "List SSH keys")
    ssh_keys = utl.do_get("ssh-keys", ctx)
    utl.cli_json_output(ssh_keys)


@click.command()
@click.pass_context
@click.option("--name", required=True, help="Name of the new ssh key to be created")
@click.option(
    "--public_key", default=None, help="Contents of the public key to be added"
)
def add(ctx, name, public_key):
    utl.cli_message(ctx, "Add SSH key")
    payload = {"name": name}
    if public_key:
        payload["public_key"] = public_key
    ssh_key = utl.do_post("ssh-keys", ctx, payload)
    utl.cli_json_output(ssh_key)


@click.command()
@click.pass_context
@click.option("--id", required=True, help="The id of ssh key to be deleted")
def delete(ctx, id):
    utl.cli_message(ctx, f"Deleting SSH key {id}")
    deleted_ssh_key = utl.do_delete(f"ssh-keys/{id}", ctx)
    utl.cli_json_output(deleted_ssh_key)


ssh.add_command(list)
ssh.add_command(add)
ssh.add_command(delete)
