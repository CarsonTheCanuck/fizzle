import click
from .util import build
from .server import serve


@click.group()
def cli():
    pass


@cli.command('build')
@click.option('--source', '-s', default='.', help='Website source directory')
@click.option('--destination', '-d', default='./_site', help='TODO OR SOMETHING')
def build_command(source, destination):
    build(source, destination)


@cli.command('serve')
@click.option('--source', '-s', default='.', help='Source directory.')
@click.option('--output', '-o', default='./_site', help='Output directory.')
@click.option('--host', '-h', default='127.0.0.1', help='Allow requests from this host.')
@click.option('--port', '-p', default=4444, help='Listen on this port.')
#@click.option('--watch', '-w', default=False, help='Watch source directory for changes and rebuild.')
def serve_command(source, output, host, port, watch=False):
    # TODO: If watch is true, start a background thread that watches for changes
    # and calls build on each change.
    #
    # Might be smart to kill a running thread in the case multiple changes
    # happen quickly.  Kill the previous incomplete thread.
    build(source, output)
    serve(output, host, port)
