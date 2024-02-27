import click
import os

from . import instance_cmd
from . import ssh_cmd
from . import fs_cmd


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj["API_KEY"] = os.environ["LAMBDALABS_API_KEY"]


cli.add_command(instance_cmd.instance)
cli.add_command(ssh_cmd.ssh)
cli.add_command(fs_cmd.fs)


def cli_launch():
    cli(obj={})
