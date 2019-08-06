import click
from flask.cli import with_appcontext

from price_app.scripts import csv_to_sql, csv_to_pandas


@click.command('csv-to-sql')
@click.argument("file_path")
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--quotechar', default='"', help='CSV quotechar')
@with_appcontext
def csv_to_sql_command(file_path, delimiter, quotechar):
    """Create SQL records with a CSV file of property listings."""
    click.echo('Processing {}'.format(file_path))
    csv_to_sql.process_csv(file_path, delimiter, quotechar)
    click.echo('Processing complete.')


@click.command('csv-to-pandas')
@click.argument("file_path")
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--quotechar', default='"', help='CSV quotechar')
@with_appcontext
def csv_to_pandas_command(file_path, delimiter, quotechar):
    """Create pandas output with a CSV file of property listings."""
    click.echo('Processing {}'.format(file_path))
    csv_to_pandas.process_csv(file_path, delimiter, quotechar)
    click.echo('Processing complete.')
