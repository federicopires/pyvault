# Pyvault

This is a tool to interact with Hashicorp's Vault KV secret engine (v1).

It supports importing a YAML file into vault, and also dumping Vault's keys with YAML formatting.

## Requirements

* [hvac](https://github.com/ianunruh/hvac)
* [pyyaml](https://github.com/yaml/pyyaml)
* [Click](http://click.pocoo.org)

## Usage

```
python3.6 pyvault.py --help
Usage: pyvault.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  read   Dumps key values from vault in YAML format.
  write  Writes contents of a YAML file to vault.
```
