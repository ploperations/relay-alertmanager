#!/usr/bin/env python3

from pdpyras import APISession
from relay_sdk import Interface, Dynamic as D
import json

relay = Interface()
token = relay.get(D.connection.accessToken)
from_address = relay.get(D.fromAddress)
session = APISession(token, default_from=from_address)

incident_id = relay.get(D.incidentId)
alert_severity = relay.get(D.alertSeverity)
default_priority = relay.get(D.defaultPriority)


def get_priorities():
    request = session.list_all('priorities')
    machine_data = {}
    human_data = {}
    for priority in request:
        name = priority['name']
        human_data[name] = {}
        human_data[name]['id'] = priority['id']
        human_data[name]['description'] = priority['description']
        machine_data[name] = priority
    print(json.dumps(human_data, indent=2))
    return machine_data


def set_priority(machine_data):
    priority = ''
    if alert_severity in machine_data:
        priority = alert_severity
    else:
        priority = machine_data[default_priority]
    print("Setting priority of incident {_id} to {_pname} / {_pid}".format(
        _id=incident_id,
        _pname=machine_data[priority]['name'],
        _pid=machine_data[priority]['id']))
    print("putting this data:")
    print({'type': 'incident', 'priority': machine_data[priority]})
    session.rput(
        'incidents/{}'.format(incident_id),
        json={'type': 'incident', 'priority': machine_data[priority]})


if __name__ == '__main__':
    data = get_priorities()
    set_priority(data)
