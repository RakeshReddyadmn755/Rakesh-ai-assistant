from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat import ask_question
import uvicorn

app = FastAPI()

# Allow CORS for all origins temporarily (replace * with frontend URL in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://your-frontend.vercel.app"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        if not question:
            return {"error": "Question is required."}

        answer = ask_question(question)

        return {"answer": answer}
    except Exception as e:
        print(f"[ERROR] /ask endpoint failed: {str(e)}")
        return {"error": f"Internal Server Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
