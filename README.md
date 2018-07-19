# dd-check-memsql
This is Agent Check for Datadog for collecting metrics of MemSQL Cluster.

:warning: This was tested only with Datadog Agent version 6
:warning: Datadog Custom Check names should not conflict with Python
          library names. Since we are able to do `import memsql`
          we need to name the custom check something else.

## Installation
Install MemSQL client.

```
$ sudo /opt/datadog-agent/embedded/bin/pip install memsql
```

And deploy this script into `checks.d/` folder.

```
$ sudo cp ./checks.d/memsql.py /etc/dd-agent/checks.d/memsqldd.py
```

Create a file `memsql.yaml` in the Agent's `conf.d/` folder.

```
$ sudo cp ./conf.d/memsql.yaml.example /etc/dd-agent/conf.d/memsqldd.d/conf.yaml
```

## Development

```console
# Install datadog-agent version 6
# Follow instructions here: https://docs.datadoghq.com/agent/
# Install dependencies
$ sudo /opt/datadog-agent/embedded/bin/pip install memsql
# symlink script and config to dadadog-agent config directory
$ ./script/bootstrap

# run dd-check-memsql
$ datadog-agent check memsqldd
```

## License
This project is releases under the [MIT license](http://opensource.org/licenses/MIT).
