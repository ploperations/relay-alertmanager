#!/usr/bin/env python3

from relay_sdk import Interface, Dynamic as D

relay = Interface()
alerts = relay.get(D.alerts)


def message_from_alerts():
    message_body = ''
    message_body += "⚠️ *{alert_name}* ⚠️\n".format(
        alert_name=alerts[0]['labels']['alertname'])
    for alert in alerts:
        message_body += "status: {status}\n".format(status=alert['status'])
        message_body += "started at: {starts_at}\n".format(starts_at=alert['startsAt'])
        message_body += "annotations:\n"
        for k, v in alert['annotations'].items():
            message_body += "  - {key}: {value}\n".format(key=k, value=v)
        message_body += "Generator URL: <{generator_url}|link>\n".format(
            generator_url=alert['generatorURL'])
        message_body += "\n"
    return message_body


if __name__ == '__main__':
    message_body = message_from_alerts()
    relay.outputs.set("message_body", message_body)
    print(message_body)
