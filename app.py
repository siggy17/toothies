from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

app = FastAPI()

model_name = "LyraLongPaw7/toothies"  # Replace with your model's Hugging Face path
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

class ChatRequest(BaseModel):
    user_input: str

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
                chatBox.innerHTML += `<p><strong>GPT-2:</strong> ${data.response}</p>`;
                document.getElementById("user-input").value = "";
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat(request: ChatRequest):
    response = text_generator(request.user_input, max_length=50, truncation=True)
    return {"response": response[0]['generated_text']}
