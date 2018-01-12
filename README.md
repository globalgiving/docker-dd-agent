# Datadog Agent for Docker
GlobalGiving uses Datadog for monitoring all of our infrastructure, including things in docker.  We found that many of the Datadog agent checks do not actually work in a containerized environment without either violating the one-process-per-container ideology, or installing 3rd party plugins/patches into the software we wanted to monitor.

These checks are designed to extend the existing ones already in the Datadog Agent, so that they can benefit from new features and bug fixes that Datadog implements in their own code.

## Quick Start

This image works just like the official Datadog Agent (infact it is just an extension of it).

If you are running stand-alone docker:

```
docker run -d --name dd-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e API_KEY={your_api_key_here} \
  -e SD_BACKEND=docker \
  -e NON_LOCAL_TRAFFIC=false \
  datadog/docker-dd-agent:latest
```

If you are using docker swarm:

```
docker service create \
  --name dd-agent \
  --mode global \
  --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
  --mount type=bind,source=/proc/,target=/host/proc/,ro=true \
  --mount type=bind,source=/sys/fs/cgroup/,target=/host/sys/fs/cgroup,ro=true \
  --publish 8125:8125/udp \
  -e API_KEY={your_api_key_here} \
  -e SD_BACKEND=docker \
  datadog/docker-dd-agent:latest
```

If you are running on Amazon Linux, use the following instead:

```
docker run -d --name dd-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /cgroup/:/host/sys/fs/cgroup:ro \
  -e API_KEY={your_api_key_here} \
  -e SD_BACKEND=docker \
  -e NON_LOCAL_TRAFFIC=false \
  datadog/docker-dd-agent:latest
```

## Enabling Checks

### Varnish

Extends the normal `varnish` check to allow `varnishstat` to be run inside the varnish container.

If you are running standalone docker, add this to your `docker run` command:

```
--label com.datadoghq.ad.check_names='["docker_varnish"]' --label com.datadoghq.ad.init_configs='[{}]' --label com.datadoghq.ad.instances='[{"varnishstat":"/usr/bin/varnishstat","container-name":"%%container-name%%"}]'
```

If you are running docker swarm, add this to your `docker service create` command:

```
--container-label com.datadoghq.ad.check_names='["docker_varnish"]' --container-label com.datadoghq.ad.init_configs='[{}]' --container-label com.datadoghq.ad.instances='[{"varnishstat":"/usr/bin/varnishstat","container-name":"%%container-name%%"}]'
```

## Other Configuration

Basically everything you can do with the normal Datadog Docker Agent, you can do with this.  So see their documentation: https://hub.docker.com/r/datadog/docker-dd-agent/

## Security Implications?

If you look at how these checks work, they allow a command to be run in the container you want to monitor by using `docker exec`.  You may be wondering if this opens any security problems.

The ability to `docker exec` from the dd-agent container to another container was already present and we did not add this.  If someone is able to gain unauthorized access to either the official dd-agent container or to your docker host system, they would already have had this power.

