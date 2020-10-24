# Alertmanager Integration for Relay.sh

This integration allows you to connect Prometheus Alertmanager to Relay.

## Steps

| Name                                                                         | Description                                                                                                                                                     |
|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [append-pagerduty-incident-link](steps/append-pagerduty-incident-link)       | This step appends a hyperlink to a PagerDuty incident to a message                                                                                              |
| [determine-service](steps/determine-service)                                 | This step determines what PagerDuty service to map an alert to                                                                                                  |
| [generate-pagerduty-custom-detials](steps/generate-pagerduty-custom-detials) | This step generates the table that is shown in the Custom Details section of a PagerDuty incident                                                               |
| [generate-pagerduty-links](steps/generate-pagerduty-links)                   | This step generates links from a PagerDuty incident to information in the system that generated each alert.                                                     |
| [generate-slack-message-consumer](steps/generate-slack-message-consumer)     | This step creates a message to be sent to consumers of a service. This message is focused on end users instead of technical operators.                          |
| [generate-slack-message-owner](steps/generate-slack-message-owner)           | This step creates a message to be sent to the operators of a service. This message includes much more technical information than an end user would want to see. |
| [get-pagerduty-incident](steps/get-pagerduty-incident)                       | This step queries PagerDuty to find the id of incident triggered by the [PagerDuty event-send](https://relay.sh/steps/pagerduty/event-send) step.               |
| [set-pagerduty-priority](steps/set-pagerduty-priority)                       | This step sets a PagerDuty priority on an incident based on information in an Alertmanager alert.                                                               |

## Triggers

| Name                                       | Description                                   |
|--------------------------------------------|-----------------------------------------------|
| [webhook-receiver](steps/webhook-receiver) | Trigger to handle a webhook from Alertmanager |

## Workflows

| Name                                 | Description                                                                |
|--------------------------------------|----------------------------------------------------------------------------|
| [example1.yaml](workflows/example1/) | This workflow shows you how to link the Foobar steps and triggers together |

## Contributing

### Issues

Feel free to submit issues and enhancement requests.

### Contributing Code

In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

### License

As indicated by the repository, this project is licensed under Apache 2.0.
