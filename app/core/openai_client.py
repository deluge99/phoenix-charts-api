import os

from openai import AsyncOpenAI

# Load .env if available to pick up OPENAI_API_KEY
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please export it or add it to your .env before starting the server."
    )

client = AsyncOpenAI(api_key=api_key)


async def openai_stream_chat(messages: list[dict], model: str = "gpt-4o-mini"):
    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {str(e)}"
