# es-cli
Elasticsearch command line tool.

_Needs python 3+_

# Configuration
_Configuration is stored in `~/.es/config`_.

To run `es`, you must first configure it, by choosing a config to use:

`es use <configuration name>`

Configure then at least an Elasticsearch cluster url:

`es config set url <cluster url>`

## Available commands:

* Help: `es help`, `es <sub command> help`
* Create a new index: `es index create <index_name> <index_json_definition_file>`
* Reindex (asynchornous): `es reindex <old_index> <new_index>`
* Tasks progression: `es task <task id>` (Ctrl+C to stop)

