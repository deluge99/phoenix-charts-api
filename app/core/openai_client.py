import asyncio
import openai
from fastapi import HTTPException


async def openai_stream_chat(messages: list[dict], model: str = "gpt-4o-mini"):
    try:
        stream = await openai.chat.completions.create(
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
