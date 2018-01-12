import docker
import sys
sys.path.append('/opt/datadog-agent/agent/checks.d')
import varnish
import utils.subprocess_output
from checks import AgentCheck

class Notset:
    def __repr__(self):
        return "<notset>"

notset = Notset()

def patch(target, name, value=notset):
    import inspect
    oldval = getattr(target, name, notset)

    # avoid class descriptors like staticmethod/classmethod
    if inspect.isclass(target):
        oldval = target.__dict__.get(name, notset)
    setattr(target, name, value)
    return oldval

class DockerVarnish(varnish.Varnish):
    def check(self, instance):
        def get_docker_exec_output(command, log, raise_on_empty_output=True):
            client = docker.from_env()
            eid = client.exec_create(instance.get('container-name'), command)
            output = client.exec_start(eid)
            return (output, "", 0)
        oldval = patch(utils.subprocess_output, 'get_subprocess_output', get_docker_exec_output)
        varnish.Varnish.check(self, instance)
        patch(utils.subprocess_output, 'get_subprocess_output', oldval)

