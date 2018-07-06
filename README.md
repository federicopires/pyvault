# Pyvault

This is a tool to interact with [Hashicorp's Vault](https://www.vaultproject.io/) KV secret engine (v1).

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

Example YAML file with strings, lists and dicts as values:

```
vault.yaml

secret/foo:
  key: password
  key2:
  - password2
  - password3
secret/bar:
  key:
    subkey: password
    subkey2: password2
```

Now, let's write that into vault:

```
export VAULT_ADDR='http://127.0.0.1:8200'
export VAILT_TOKEN=some-token

pyvault write vault.yaml
```

Here's how it looks in vault:

```
vault kv get secret/foo

Key     Value
---     -----
key     password
key2    [password2 password3]

vault kv get secret/bar

=== Data ===
Key    Value
---    -----
key    map[subkey:password subkey2:password2]
```
