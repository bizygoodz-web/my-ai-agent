from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Explain LangGraph, CrewAI and AutoGen. Which should I learn first?"}]
)

print(response.choices[0].message.content)
