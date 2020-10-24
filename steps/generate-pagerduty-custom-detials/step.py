#!/usr/bin/env python3

from relay_sdk import Interface, Dynamic as D
import json

relay = Interface()
alerts = relay.get(D.alerts)


def custom_details_from_alerts():
    custom_details = {}
    custom_details['alert_name'] = alerts[0]['labels']['alertname']
    firing_count = 0
    resolved_count = 0
    for alert in alerts:
        if alert['status'] == 'firing':
            firing_count += 1
            alert_key = "alert-{}".format(str(firing_count))
            alert_value = ''
            alert_value += "status: {status}\n".format(status=alert['status'])
            alert_value += "started at: {starts_at}\n".format(starts_at=alert['startsAt'])
            alert_value += "annotations:\n"
            for k, v in alert['annotations'].items():
                alert_value += "  - {key}: {value}\n".format(key=k, value=v)
            alert_value += "Generator URL: {generator_url}\n".format(
                generator_url=alert['generatorURL'])
            alert_value += "\n"
            custom_details[alert_key] = alert_value
        elif alert['status'] == 'resolved':
            resolved_count += 1
    return custom_details


if __name__ == '__main__':
    custom_details = custom_details_from_alerts()
    relay.outputs.set("custom_details", custom_details)
    print(json.dumps(custom_details, indent=2))
