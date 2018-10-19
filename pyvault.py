import os
import sys
import hvac
import yaml
import click

from getpass import getpass


@click.group()
def cli():
    pass


@cli.command(help='Writes contents of a YAML file to vault.')
@click.argument('filename', type=click.Path(exists=True))
@click.option('--userpass', is_flag=True, default=False,
              help='Use userpass auth backend instead of token.')
@click.option('--tls_skip_verify', is_flag=True, default=True,
              help='Skip ssl certificate verification')
def write(filename, tls_skip_verify, userpass):
    """
    Writes dict built from YAML file to vault.
    :param filename: path to YAML file
    :param tls_skip_verify: true/false to enable/disable ssl cert verification
    :param userpass: true/false to enable/disable userpass auth backend
    :return:
    """

    client = _vault_connect(tls_skip_verify, userpass)
    data = _load_yaml(filename)

    for path, kv in data.items():

        kv = _sanitize_dict(kv)

        try:
            client.write(path, **kv)
        except Exception as e:
            print('Error writing to vault: %s' % e)
            sys.exit(1)


@cli.command(help='Dumps key values from vault in YAML format.')
@click.argument('path')
@click.option('--userpass', is_flag=True, default=False,
              help='Use userpass auth backend instead of token.')
@click.option('--tls_skip_verify', is_flag=True, default=True,
              help='Skip ssl certificate verification')
def read(path, tls_skip_verify, userpass):
    """
    Reads from vault key at the given path and dumps values.
    :param path: path to the key in vault
    :param tls_skip_verify: true/false to enable/disable ssl cert verification
    :param userpass: true/false to enable/disable userpass auth backend
    :return:
    """

    client = _vault_connect(tls_skip_verify, userpass)
    d = {path: {}}

    try:
        data = client.read(path)['data']
    except Exception as e:
        print('Error reading from vault: %s' % e)
        sys.exit(1)

    for key, value in data.items():
        d[path][key] = value

    # Adapt the Representer to output all strings with embedded newlines
    # using the literal scalar block style
    # (assuming they don't need \ escaping of special characters,
    # which will force double quotes).
    # This fixes extra newlines in yaml scalars.
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
    yaml.add_representer(str, _repr_str, Dumper=yaml.SafeDumper)

    print(yaml.dump(d, default_flow_style=False))


def _repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str',
                                       data, style='|')
    return dumper.org_represent_str(data)


def _vault_connect(tls_skip_verify=True, userpass=False):
    """
    Connects to vault using env vars for address and token, or userpass auth.
    :return: vault client object
    :param tls_skip_verify: true/false to enable/disable ssl cert verification
    :param userpass: true/false to enable/disable userpass auth backend
    """

    if userpass:
        try:
            username = input('Vault username: ')
            password = getpass(prompt='Vault password: ')
            client = hvac.Client(url=os.environ['VAULT_ADDR'],
                                 verify=tls_skip_verify)
            client.auth_userpass(username, password)
        except Exception as e:
            print('Error connecting to vault: %s' % e)
            sys.exit(1)
    else:
        try:
            client = hvac.Client(url=os.environ['VAULT_ADDR'],
                                 token=os.environ['VAULT_TOKEN'],
                                 verify=tls_skip_verify)
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
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                print("YAML error at position: (%s:%s) in %s: %s" %
                      (mark.line + 1, mark.column + 1, filename, e))
            else:
                print('Error while loading YAML file: %s' % e)
            sys.exit(1)

    return data


def _sanitize_dict(data):
    """
    Make sure dict's keys are strings (vault requirement)
    :param data: dictionary
    :return: sanitized dictionary
    """
    for k, v in data.items():
        if not isinstance(k, str):
            data[str(k)] = data.pop(k)

    return data


if __name__ == '__main__':
    cli()
