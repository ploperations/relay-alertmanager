#!/usr/bin/env python3

from pdpyras import APISession
from relay_sdk import Interface, Dynamic as D
import json

relay = Interface()
token = relay.get(D.connection.accessToken)
session = APISession(token)

alert_name = relay.get(D.alert_name)
service_name = relay.get(D.service_name)


def get_pd_incident():
    print("alert_name: {}".format(alert_name))
    print("service_name: {}".format(service_name))

    incident_list = session.list_all(
        'incidents',
        params={'statuses[]': ['triggered', 'acknowledged']})

    pd_incident_id = 'not found'
    pd_html_url = 'not found'
    for i in incident_list:
        t = i['title']
        s = i['service']['summary'].lower()
        if t == alert_name and s == service_name:
            print('Matching incident found:')
            print(json.dumps(i, indent=2))
            pd_incident_id = i['incident_id']
            pd_html_url = i['html_url']
            break
    return {
        'pd_incident_id': pd_incident_id,
        'pd_html_url': pd_html_url
    }


if __name__ == '__main__':
    data = get_pd_incident()
    relay.outputs.set("pd_incident_id", data['pd_incident_id'])
    relay.outputs.set("pd_html_url", data['pd_html_url'])
    print("pd_incident_id: {}".format(data['pd_incident_id']))
    print("pd_html_url: {}".format(data['pd_html_url']))
