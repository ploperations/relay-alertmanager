#!/usr/bin/env python3

from relay_sdk import Interface, Dynamic as D

relay = Interface()
jira_ticket = relay.get(D.jiraTicket)
input_message = relay.get(D.inputMessage)


def append_jira_ticket_to_message():
    message_body = ''
    message_body += input_message
    message_body += "\n"
    message_body += jira_ticket
    return message_body


if __name__ == '__main__':
    message_body = append_jira_ticket_to_message()
    relay.outputs.set("message_body", message_body)
    print(message_body)
