#!/usr/bin/env python3

from relay_sdk import Interface, Dynamic as D
import json

relay = Interface()
alerts = relay.get(D.alerts)

# This should be a dictionary with keys equal to
# service names and values equal to destinations.
# The dictionary should contain the key 'default_service'
# with values corresponding to the default notification
# destinations.
known_services = relay.get(D.known_services)


def service_name_from_alerts():
    if 'service' in alerts[0]['labels']:
        service_label = alerts[0]['labels']['service']
    else:
        service_label = 'unknown'
    if service_label in known_services:
        service_name = service_label
    else:
        service_name = 'default_service'
    return service_name


if __name__ == '__main__':
    service_name = service_name_from_alerts()
    if service_name == 'default_service' and 'name' in known_services[service_name]:
        relay.outputs.set("service_name", known_services[service_name]['name'])
    else:
        relay.outputs.set("service_name", service_name)
    if "pagerduty_connection" in known_services[service_name]:
        relay.outputs.set(
            "service_name_pd_connection",
            known_services[service_name]['pagerduty_connection'])
    relay.outputs.set("service_notifications", known_services[service_name])
    print("service_name: {}".format(service_name))
