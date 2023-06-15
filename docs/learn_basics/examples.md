

## BPMN Model

## Exclusive Gateway

Exclusive Gateways are used when exactly one alternative can be selected.

Suppose our products are T-shirts and we offer product C in several colors. After the user selects a product, we check to see it if is customizable. Our default branch will be 'Not Customizable', but we'll direct the user to a second form if they select 'C'; our condition for choosing this branch is a simple python expression.

![figures/gateways/exclusive_gateway.png](https://github.com/sartography/SpiffWorkflow/raw/main/doc/bpmn/figures/gateways/exclusive_gateway.png)
## Parallel Gateway

Parallel Gateways are used when the subsequent tasks do not need to be completed in any particular order. The user can complete them in any sequence and the workflow will wait for all tasks to be finished before advancing.

We do not care whether the user chooses a shipping method or enters their address first, but they'll need to complete both tasks before continuing.

We don't need to do any particular configuration for this gateway type.

[![figures/gateways/parallel_gateway.png](https://github.com/sartography/SpiffWorkflow/raw/main/doc/bpmn/figures/gateways/parallel_gateway.png)](https://github.com/sartography/SpiffWorkflow/blob/main/doc/bpmn/figures/gateways/parallel_gateway.png)

## Inclusive Gateway

SpiffWorkflow also supports Inclusive Gateways, though we do not have an example of this gateway type in this tutorial. Inclusive Gateways have conditions on outgoing flows like Exclusive Gateways, but unlike Exclusive Gateways, multiple paths may be taken if more than one conition is met.

https://www.modernanalyst.com/Careers/InterviewQuestions/tabid/128/ID/2602/Describe-the-BPMN-Inclusive-Gateway-and-how-it-is-used-in-process-modeling.aspx


## Event-Based Gateway

SpiffWorkflow supports Event-Based Gateways, though we do not use them in this tutorial. Event-Based gateways select an outgoing flow based on an event. We'll discuss events in the next section.
https://docs.camunda.org/manual/7.19/reference/bpmn20/gateways/event-based-gateway/
