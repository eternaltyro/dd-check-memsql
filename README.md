# dd-check-memsql
This is Agent Check for Datadog for collecting metrics of MemSQL Cluster.

:warning: This was tested only with Datadog Agent version 6
:warning: Datadog Custom Check names should not conflict with Python
          library names. Since we are able to do `import memsql`
          we need to name the custom check something else.

## Installation

Install supporting libraries

```
$ sudo apt install libmysqlclient-dev
```

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

Restart Datadog agent

```
# Use any relevant service manager
$ sudo systemctl restart datadog-agent
```

## Verification

Check health of Datadog-Agent

```
root@ip-172-1-2-10:/home/ubuntu# datadog-agent health
Agent health: PASS
=== 11 healthy components ===
ad-autoconfig, ad-configresolver, aggregator, collector-queue, dogstatsd-main, forwarder, healthcheck, metadata-agent_checks, metadata-host, metadata-resources, tagge
```

Validate configuration

```
=== memsqldd check ===
Source: File Configuration Provider
Instance 1:
host: 127.0.0.1
port: 3306
user: root
~
===
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
