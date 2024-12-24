import re
import asyncio

from config import OPENAI_API_KEY, OPENAI_ASSISTANT_ID
from openai import OpenAI

# client = OpenAI(
#     api_key="xai-2r6KLN9WH3QXXGbnsoGT2WWxAHtOvI6LoS51lrRjmVEi37EmUd1BxKFLhtS0DQSNZGUo5OskoyFSvxdj",
#     base_url="https://api.x.ai/v1",
# )

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1",
)


def clear_context(text):
    return re.sub(r"【.*】", "", text)


async def get_answer_async(request, thread):
    client.beta.threads.messages.create(thread.id, role="user", content=request)

    run = await asyncio.to_thread(
        lambda: client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=OPENAI_ASSISTANT_ID
        )
    )

    if run.status == "completed":
        response = client.beta.threads.messages.list(thread.id, limit=1)
        return clear_context(response.data[0].content[0].text.value)
    else:
        return "Извините, произошла ошибка."
