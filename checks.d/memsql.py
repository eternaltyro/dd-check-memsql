from checks import AgentCheck
from contextlib import contextmanager

# 3rd party
from memsql.common import database

class MemSQL(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        host, port, user, password = self._get_config(instance)
        with self._connect(host, port, user, password) as db:
            try:
                is_aggregator = self._submit_status(db)
                if is_aggregator:
                    self._submit_leaves(db)
                    self._submit_aggregators(db)
                    self._submit_cluster_status(db)
            except Exception as e:
                self.log.error("fail to send metrics to datadog")

    def _get_config(self, instance):
        self.host = instance.get('host', '')
        self.port = int(instance.get('port', 3306))
        user = instance.get('user', '')
        password = instance.get('password', '')

        return (self.host, self.port, user, password)

    @contextmanager
    def _connect(self, host, port, user, password):
        db = None
        try:
            db = database.connect(host=host, port=port, user=user, password=password)
            self.log.debug("Connected to MemSQL")
            yield db
        except Exception:
            raise
        finally:
            if db:
                db.close()

    def _submit_status(self, db):
        try:
            res = db.query('SHOW STATUS;')
            is_aggregator = False
            if res is not None:
                for i in res:
                    variable_name = i['Variable_name'].lower()
                    if variable_name == 'aggregator_id':
                        is_aggregator = True
                    elif variable_name == 'threads_connected':
                        self.count('memsql.current_connections', int(i['Value']))

            return is_aggregator
        except Exception as e:
            self.log.error("fail to execute _submit_status")
            return None

    def _submit_leaves(self, db):
        try:
            res = db.query('SHOW LEAVES;')
            if res is not None:
                online_leaves = 0
                for i in res:
                    if i['State'] == 'online':
                        online_leaves += 1
                    if i['Average_Roundtrip_Latency_ms'] is not None:
                        self.gauge('memsql.roundtrip_latency', i['Average_Roundtrip_Latency_ms'], tags=["memsql_target_host:"+i['Host']])
                self.count('memsql.leaves', len(res))
                self.count('memsql.online_leaves', online_leaves)

        except Exception as e:
            self.log.error("fail to execute _submit_leaves")
            return None

    def _submit_aggregators(self, db):
        try:
            res = db.query('SHOW AGGREGATORS;')
            if res is not None:
                master_aggregators = 0
                online_master_aggregators = 0
                child_aggregators = 0
                online_child_aggregators = 0
                for i in res:
                    if int(i['Master_Aggregator']) == 1:
                        master_aggregators += 1
                        if i['State'] == 'online':
                            online_master_aggregators += 1
                    else:
                        child_aggregators += 1
                        if i['State'] == 'online':
                            online_child_aggregators += 1
                    
                    if i['Average_Roundtrip_Latency_ms'] is not None:
                        self.gauge('memsql.roundtrip_latency', i['Average_Roundtrip_Latency_ms'], tags=["memsql_target_host:"+i['Host']])

                self.count('memsql.master_aggregators', master_aggregators)
                self.count('memsql.online_master_aggregators', online_master_aggregators)
                self.count('memsql.child_aggregators', child_aggregators)
                self.count('memsql.online_child_aggregators', online_child_aggregators)

        except Exception as e:
            self.log.error("fail to execute _submit_aggregators")
            return None

    def _submit_cluster_status(self, db):
        try:
            res = db.query('SHOW CLUSTER STATUS;')
            if res is not None:
                references = 0
                partitions = 0
                online_partitions = 0
                for i in res:
                    if i['Role'] == 'Reference':
                        references += 1
                    else:
                        partitions += 1
                        if i['State'] == 'online':
                            online_partitions += 1
                self.count('memsql.references', references)
                self.count('memsql.partitions', partitions)
                self.count('memsql.online_partitions', online_partitions)

        except Exception as e:
            self.log.error("fail to execute _submit_cluster_status")
            return None
