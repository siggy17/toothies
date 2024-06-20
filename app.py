from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/your-username/your-model"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

class ChatRequest(BaseModel):
    user_input: str

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.get("/", response_class=HTMLResponse)
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat with GPT-2</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .chat-container {
                width: 100%;
                max-width: 500px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            .chat-box {
                width: 100%;
                height: 300px;
                border: 1px solid #ccc;
                border-radius: 10px;
                overflow-y: auto;
                padding: 10px;
                margin-bottom: 10px;
            }
            .input-box {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            .send-button {
                width: 100%;
                padding: 10px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-box" id="chat-box"></div>
            <textarea class="input-box" id="user-input" placeholder="Type your message here..."></textarea>
            <button class="send-button" onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                const userInput = document.getElementById("user-input").value;
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ user_input: userInput })
                });
                const data = await response.json();
                const chatBox = document.getElementById("chat-box");
                chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
                chatBox.innerHTML += `<p><strong>GPT-2:</strong> ${data.response[0]['generated_text']}</p>`;
                document.getElementById("user-input").value = "";
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat(request: ChatRequest):
    data = query({"inputs": request.user_input})
    return {"response": data}
