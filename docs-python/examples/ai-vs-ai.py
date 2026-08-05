import uuid
from random import sample
from time import sleep

from langchain_classic.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from gen_ai_hub.proxy.langchain.amazon import ChatBedrock
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

store = {}

available_models = [
    {
        "model_class": ChatBedrock,
        "model_kwargs": {"model_name": "amazon--titan-text-express"},
        "speaking_name": "Amazon Titan Text Express",
    },
    {
        "model_class": ChatBedrock,
        "model_kwargs": {"model_name": "anthropic--claude-3-haiku"},
        "speaking_name": "Anthropic Claude 3 Haiku",
    },
    {
        "model_class": ChatOpenAI,
        "model_kwargs": {"proxy_model_name": "gpt-4o-mini"},
        "speaking_name": "GPT 4o mini",
    },
]


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def create_session_history() -> str:
    session_id = str(uuid.uuid4())
    store[session_id] = ChatMessageHistory()
    return session_id


def create_instructed_model(base_model, speaking_name, session_id):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the large language model {llmname}. Your goal is to answer questions nicely and keep a conversation going. Add a creative question unrelated to the previous conversaiton at the end of your answer. Also do everything with a pirate accent!",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    model = prompt | base_model
    return {
        "model": model,
        "speaking_name": speaking_name,
        "session_id": session_id,
    }


def converse_ai(model_dict, prompt) -> str:
    config = {"configurable": {"session_id": model_dict["session_id"]}}
    model = model_dict["model"]
    model_with_message_history = RunnableWithMessageHistory(
        model,
        get_session_history,
        input_messages_key="messages",
    )
    response = model_with_message_history.invoke(
        {
            "messages": [HumanMessage(content=prompt)],
            "llmname": model_dict["speaking_name"],
        },
        config=config,
    )
    return response.content


def main():
    session_id_model_1 = create_session_history()
    session_id_model_2 = create_session_history()

    model_1, model_2 = sample(available_models, 2)

    model_1 = create_instructed_model(
        model_1["model_class"](**model_1["model_kwargs"]),
        speaking_name=model_1["speaking_name"],
        session_id=session_id_model_1,
    )
    model_2 = create_instructed_model(
        model_2["model_class"](**model_2["model_kwargs"]),
        speaking_name=model_2["speaking_name"],
        session_id=session_id_model_2,
    )

    model_of_last_turn = model_1
    model_of_next_turn = model_2
    last_response = "Introduce yourself."
    for _ in range(1, 11):
        last_response = converse_ai(model_of_next_turn, last_response)
        print("#########################################################")
        print(model_of_next_turn["speaking_name"] + ": " + last_response)
        print("#########################################################")
        model_of_next_turn, model_of_last_turn = model_of_last_turn, model_of_next_turn
        sleep(3)


if __name__ == "__main__":
    main()
