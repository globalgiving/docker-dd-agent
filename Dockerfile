FROM datadog/docker-dd-agent:latest-jmx
MAINTAINER Justin Rupp <jrupp@globalgiving.org>

COPY checks/docker_varnish.py /etc/dd-agent/checks.d/

