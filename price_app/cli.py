import click
from flask.cli import with_appcontext

from price_app.scripts.process_csv import process_csv


@click.command('process-csv')
@click.argument("file_path")
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--quotechar', default='"', help='CSV quotechar')
@with_appcontext
def process_csv_command(file_path, delimiter, quotechar):
    """Process a CSV file of property listings."""
    click.echo('Processing {}'.format(file_path))
    process_csv(file_path, delimiter, quotechar)
    click.echo('Processing complete.')
