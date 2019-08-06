import click
from flask.cli import with_appcontext

from price_app.scripts.csv_to_sql import process_csv


@click.command('csv-to-sql')
@click.argument("file_path")
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--quotechar', default='"', help='CSV quotechar')
@with_appcontext
def csv_to_sql_command(file_path, delimiter, quotechar):
    """Create SQL records with a CSV file of property listings."""
    click.echo('Processing {}'.format(file_path))
    process_csv(file_path, delimiter, quotechar)
    click.echo('Processing complete.')
