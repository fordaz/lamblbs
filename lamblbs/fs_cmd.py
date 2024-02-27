import click
from . import cmd_utils as utl


@click.group()
@click.pass_context
@click.option("--json_output", is_flag=True, default=False)
def fs(ctx, json_output):
    ctx.obj["JSON_OUTPUT"] = json_output


@click.command()
@click.pass_context
def list(ctx):
    utl.cli_message(ctx, "List File Systems")
    ssh_keys = utl.do_get("file-systems", ctx)
    utl.cli_json_output(ssh_keys)


fs.add_command(list)
