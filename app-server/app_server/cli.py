import click
from flask.cli import with_appcontext

from app_server.scripts import csv_to_pandas


@click.command('csv-to-pandas')
@click.argument("file_path")
@click.option('--delimiter', default=',', help='CSV delimiter')
@click.option('--quotechar', default='"', help='CSV quotechar')
@click.option('--save', default='csv', help='Save type. Accepts csv or mongo')
@with_appcontext
def csv_to_pandas_command(file_path, delimiter, quotechar, save):
    """
    Process CSV file of property listings, and save result.
    """
    click.echo('Processing {}'.format(file_path))
    dataframe = csv_to_pandas.process_csv(file_path, delimiter, quotechar)
    click.echo('Processing complete.')

    if save == 'csv':
        csv_filename = csv_to_pandas.save_to_csv(dataframe)
        click.echo('Saved to {}'.format(csv_filename))
    elif save == 'mongo':
        save_result = csv_to_pandas.save_to_mongo(dataframe)
        click.echo('Saved to mongo. {} records created.'.format(len(save_result.inserted_ids)))


# @click.command('csv-to-sql')
# @click.argument("file_path")
# @click.option('--delimiter', default=',', help='CSV delimiter')
# @click.option('--quotechar', default='"', help='CSV quotechar')
# @with_appcontext
# def csv_to_sql_command(file_path, delimiter, quotechar):
#     """
#     Create SQL records with a CSV file of property listings.
#     """
#     click.echo('Processing {}'.format(file_path))
#     csv_to_sql.process_csv(file_path, delimiter, quotechar)
#     click.echo('Processing complete.')
