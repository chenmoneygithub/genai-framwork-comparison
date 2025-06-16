# PydanticAI

This report is based on my experience of building the following programs with PydanticAI:

- A quickstart dummy agent, with streaming (only in notebook).
- An airline service agent, which can help users book and manage flights. It's a tool calling agent based on ReAct.

PydanticAI is specialized for building agents, so I am skipping the non-agent use cases.

## Overview

My overall comment of PydanticAI is it's a pretty solid framework. One big advantage is PydanticAI is pretty flexible,
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
| I love the code                                           | Decen                |


## Comment

### Flexible Node Control



### Powerful Streaming



### Too Many Concepts



### Decent Tracing, While Broken on Error


## Conclusion

Agno is an elegant framework for building tool-calling agents. I do recommend giving it a try if your use
case can be covered by tool-calling agents.
