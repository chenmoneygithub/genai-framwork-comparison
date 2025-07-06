# PydanticAI

This report is based on my experience of building the following programs with PydanticAI:

- A quickstart dummy agent, with streaming (only in notebook).
- An airline service agent, which can help users book and manage flights. It's a tool calling agent based on ReAct.

PydanticAI is specialized for building agents, so I am skipping the non-agent use cases.

## Overview

My overall comment of PydanticAI is it's a solid framework. One big advantage is PydanticAI is pretty flexible,
which means for users fully aware of what they are trying to do, it's a nice tool. However, on the other hand this
means a steeper learning curve than other frameworks. What I don't like the most is the massive number of concepts
introduced, while it's not super clear what these concepts are about. This can be partially told by this big chunk of
import from [the agent streaming example](https://ai.pydantic.dev/agents/#streaming):

```
from pydantic_ai.messages import (
    FinalResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
    ToolCallPartDelta,
)
```


Feature overview, from what I can find:

| Feature                                          | Supported?           | Dev Experience Or Comment    |
|--------------------------------------------------|----------------------|------------------------------|
| Agent API                                        | Y                    | Good                         |
| Prompt Writing Helper                            | N                    |                              |
| Client Cache                                     | N                    |                              |
| Tracing                                          | Y                    | Good                         |
| Output Token Streaming                           | Y                    | Decent                       |
| Intermediate Streaming<br>(Tool calling message) | Y                    | Decent                       |
| Intermediate Token Streaming                     | N                    | Very Good                    |
| Structured Output, e.g., Pydantic as output      | Y                    | Very Good                    |
| Save/Load                                        | N                    |                              |
| Automatic Prompt Optimization                    | N                    |                              |
| Runnable in Ipython                              | Y                    | Good                         |

Workflow experience:

| Workflow Name                                             | Developer Experience |
|-----------------------------------------------------------|----------------------|
| Build an Airline Service Agent,<br>which has tool calling | Good                 |
| Get streaming to work                                     | Decent               |
| Generate trace and debug with trace                       | Decent               |
| Switch LM behind the scene                                | Good                 |
| Put demo up by reading the documentation                  | Decent               |
| I love the code                                           | Decent               |


## Comment

### Flexible Node Control

PydanticAI allows users to access and control the node at execution time, as shown by the code snippet
below, which is copied from the [agent->stream tutorial](https://ai.pydantic.dev/agents/#streaming).

```python
async with weather_agent.iter(user_prompt, deps=WeatherService()) as run:
    async for node in run:
        if Agent.is_user_prompt_node(node):
            # A user prompt node => The user has provided input
            output_messages.append(f'=== UserPromptNode: {node.user_prompt} ===')
        elif Agent.is_model_request_node(node):
            ...
```

The definition of Node is not super clear on the documentation, but it's not hard to understand. Behind
the scene PydanticAI agent is a graph with multiple kinds of nodes. For example, a tool call is a node, an LM call
is also a node: https://ai.pydantic.dev/graph/. By providing access to these nodes at call time, users
can put up custom logic like streaming on intermediate execution.

This is a good feature IMO, but I would like the explanation to be more clear, and I would like to see a more clear
picture on what I can achieve by controlling these nodes with tutorials.

### Dependency Injection

Dependency system is one important part of PydanticAI: https://ai.pydantic.dev/dependencies/#accessing-dependencies.
But after reading the documentation, I am not clear about the exact goal of this dependency system. Based on my
reading, it's mostly for managing the runtime state and shared utils.

But here is something personal - I am a big hater of dependency injection. The concept is fine to me, but the reality
is horrible. Many times I have no clue where the actual instance comes from, and need to jump like 20 times to a different
file to figure it out. So PydanticAI is not something I would personally consider.

This doesn't really mean PydanticAI is a terrible framework, I am just saying this is less appealing for people not
a fan of dependency injection.

### Too Many Concepts

Simply reading the quickstart: https://ai.pydantic.dev/agents/, I am bumping into a massive number of arbitrary
concepts, including but not limited to: Agent, Node, Deps, RunContext, End, template-alike syntax
`Agent[WeatherService, str]`.

I feel the goal behind the scene to build a robust while flexible system which is ready for productization, but
it could be frustrating for users to learn all of these. One thing I want to call out is it's way easier to build
a so-called GenAI framework like PydanticAI or Langgraph than building an autograd framework like PyTorch or
Tensorflow. That means I would be cautious about the learning curve, in another word, I don't want to learn these
many concepts just in order to build the same thing.


### Decent Tracing, While Broken on Error

PydanticAI tracing is done through something called Logfire. It's pretty easy to turn on the automatic tracing

```
logfire.configure()
logfire.instrument_pydantic_ai()
```

UI-wise it's all right, but I would say it's worse than the competitors like Agno, LangFuse or MLflow, like
the hierarchy is not clear, and the display is too verbose:

![Trace](./logfire.png)

More importantly, the tracing is broken on error. I have no idea why, but the trace is not recorded.

![Error](./error.png)


## Conclusion

PydanticAI is a solid framework for building agents. It's flexible and powerful, but the learning curve is
a bit steeper than competitors like Agno or Langgraph. Personally because I am not a fan of dependency injection,
I would not consider it for my own projects.
