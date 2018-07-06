import os
import sys
import hvac
import yaml
import click


@click.group()
def cli():
    pass


@cli.command(help='Writes contents of a YAML file to vault.')
@click.argument('filename', type=click.Path(exists=True))
def write(filename):
    """
    Writes dict built from YAML file to vault.
    :param filename: path to YAML file
    :return:
    """

    client = _vault_connect()
    data = _load_yaml(filename)

    for path, kv in data.items():

        try:
            client.write(path, **kv)
        except Exception as e:
            print('Error writing to vault: %s' % e)
            sys.exit(1)


@cli.command(help='Dumps key values from vault in YAML format.')
@click.argument('path')
def read(path):
    """
    Reads from vault key at the given path and dumps values.
    :param path: path to the key in vault
    :return:
    """

    client = _vault_connect()
    d = {path: {}}

    try:
        data = client.read(path)['data']
    except Exception as e:
        print('Error reading from vault: %s' % e)
        sys.exit(1)

    for key, value in data.items():
        d[path][key] = value

    print(yaml.dump(d, default_flow_style=False))


def _vault_connect():
    """
    Connects to vault using env vars for address and token.
    :return: vault client object
    """

    try:
        client = hvac.Client(url=os.environ['VAULT_ADDR'],
                             token=os.environ['VAULT_TOKEN'])
    except Exception as e:
        print('Error connecting to vault: %s' % e)
        sys.exit(1)

    return client


def _load_yaml(filename):
    """
    Loads YAML content from filename
    :param filename: path to YAML file
    :return: dict with YAML content
    """

    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)

        except yaml.YAMLError as e:
            print('Error while loading YAML file: %s' % e)
            sys.exit(1)

    return data

if __name__ == '__main__':
    cli()
