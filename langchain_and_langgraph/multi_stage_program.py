import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from typing_extensions import TypedDict

if os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_TRACING"] = "true"

openai_model = ChatOpenAI(model_name="gpt-4o-mini")


class InputState(TypedDict):
    question: str


class OutputState(TypedDict):
    answer_and_eval: tuple[str, int]


class OverallState(TypedDict):
    question: str
    answer: str
    eval: int


class Eval(BaseModel):
    eval: int


def generate_answer(state: InputState) -> OverallState:
    prompt_template = ChatPromptTemplate([("system", "You are a helpful assistant"), ("user", "{question}")])
    messages = prompt_template.invoke({"question": state["question"]})
    return {"question": state["question"], "answer": openai_model.invoke(messages).content}


def get_eval(state: OverallState) -> OverallState:
    prompt_template = ChatPromptTemplate(
        [
            (
                "system",
                (
                    "Evaluate the quality of the answer to the user question, in a scale between 0 "
                    "to 10. Just give me the integer, no explanation needed."
                ),
            ),
            ("user", "The question: {question}, and the generated answer: {answer}"),
        ]
    )
    messages = prompt_template.invoke(
        {
            "question": state["question"],
            "answer": state["answer"],
        }
    )
    output = int(openai_model.invoke(messages).content)

    return {
        "question": state["question"],
        "answer": state["answer"],
        "eval": output,
    }


def combine(state: OverallState) -> OutputState:
    return {"answer_and_eval": (state["answer"], state["eval"])}


builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node("node_1", generate_answer)
builder.add_node("node_2", get_eval)
builder.add_node("node_3", combine)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)


graph = builder.compile()
print(graph.invoke({"question": "What is so great about basketball?"}))
