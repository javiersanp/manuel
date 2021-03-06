from __future__ import absolute_import
import click
from manuel.manuel import generate_report
from manuel.manuel import create_index


@click.group()
def manuel():
    pass


def invoke():
    manuel()


@manuel.command()
@click.argument('config_file')
@click.option('--index/--no-index', default=False)
@click.option('--debug/--no-debug', default=False)
def cli_generate_report(config_file, index, debug):
    """
    CLI entry point

    :param config_file:
    :param index:
    :param debug:
    :return:
    """
    if index:
        create_index(config_file, debug)
    generate_report(config_file, debug)
