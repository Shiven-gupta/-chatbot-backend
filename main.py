from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str
@app.post("/chat")
async def chat(msg: Message):
    prompt = f"""
 You are a helpful assistant trained only to help users explore Shiven Gupta's portfolio website.

You can help users navigate the following sections: Hero, About, Skills, Projects, Certifications, and Contact.

If someone asks about anything else, say: "I'm only trained to help with Shiven's portfolio site."

You are allowed to explain **only the skills listed in the Skills section** of the site. If a user asks about a skill that is listed, explain it clearly in simple terms.

If the skill is **not listed** on the site, respond with: "That skill is not mentioned on the portfolio."

Do not ask the user to go to the skills section. Just explain the skill if it exists on the site.

 "{msg.message}"
    """

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    body =  {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": prompt}]
    }



    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=body,
            headers=headers
        )

        try:
            data = res.json()
           
            print("Groq API response:", data)

            # Now safely access choices key
            if "choices" not in data:
                return {"reply": "AI API error: no choices in response 😓"}

            reply = data["choices"][0]["message"]["content"]
            return {"reply": reply.strip()}

        except Exception as e:
            print(f"Error parsing API response: {e}")
            return {"reply": "Yo, server broke parsing response! 🔧😩"}


    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        reply = res.json()["choices"][0]["message"]["content"]
        return { "reply": reply.strip() }

print("GROQ_API_KEY:", GROQ_API_KEY)