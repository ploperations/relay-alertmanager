#!/usr/bin/env python3

from relay_sdk import Interface, Dynamic as D

relay = Interface()
pagerduty_link = relay.get(D.pagerdutyLink)
slack_message = relay.get(D.slackMessage)


def append_pd_link_to_message():
    message_body = ''
    message_body += slack_message
    if pagerduty_link != 'not found':
        message_body += "<{}|Incident in PagerDuty>".format(pagerduty_link)
    return message_body


if __name__ == '__main__':
    message_body = append_pd_link_to_message()
    relay.outputs.set("message_body", message_body)
    print(message_body)
