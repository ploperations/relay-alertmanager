#!/usr/bin/env python3

# a webhook responder that puts the payload from Alertmanager
# into parameters used by a workflow. Each top level key in
# the payload is mapped to a parameter.

from datetime import datetime
from relay_sdk import Interface, WebhookServer
from quart import Quart, request, make_response

import json
import os

if 'METADATA_API_URL' in os.environ:
    relay = Interface()
else:
    import logging
    import sys
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    log_handler.setFormatter(formatter)
    root.addHandler(log_handler)

app = Quart('alertmanager-webhook-receiver')


def sort_by_key(data):
    return dict(sorted(data.items(), key=lambda item: item[0]))


@app.route('/', methods=['POST'])
async def handler():
    print('getting payload from request')
    payload = await request.get_json()
    fingerprints = []

    if payload is None:
        return {'message': 'not a valid webhook'}, 400, {}

    if payload["version"] != "4":
        return {'message': "Unknown message version %s" % payload["version"]}, 400, {}

    # Sort list of alerts by label values to make sure that task description
    # stays the same when Alertmanager sends the same list of alerts in a
    # different order.
    if "alerts" in payload:
        payload["alerts"] = sorted(
            payload["alerts"],
            key=lambda a: sorted(a["labels"].values())
        )
        for alert in payload["alerts"]:
            fingerprints.append(alert["fingerprint"])
        first_alert_date = payload["alerts"][0]["startsAt"]
        fingerprints.sort()
        alert_duration = (datetime.now() - datetime.strptime(first_alert_date, '%Y-%m-%dT%H:%M:%S.%fZ')).days
        fingerprint_string = "".join(fingerprints)
        fingerprint_plus_days = "{fingerprint}-{days_of_alerting}".format(
            fingerprint=fingerprint_string,
            days_of_alerting=str(alert_duration))
        payload['relay'] = {}
        payload['relay']['fingerprintString'] = fingerprint_string
        payload['relay']['fingerprintStringPlusDays'] = fingerprint_plus_days

    for k in ["commonAnnotations", "commonLabels", "groupLabels"]:
        if k in payload:
            payload[k] = sort_by_key(payload[k])

    json_formatted_str = json.dumps(payload, indent=2)

    if 'METADATA_API_URL' in os.environ:
        print("received payload:\n%s" % json_formatted_str)
        relay.events.emit(payload, key=fingerprint_string)
        # relay.events.emit(payload)
    else:
        logging.info("Got payload:\n%s", json_formatted_str)
        logging.info("Generated fingerprint: %s", fingerprint_string)
        logging.info("\n")

    return {'message': 'success'}, 200, {}

if __name__ == '__main__':
    WebhookServer(app).serve_forever()
