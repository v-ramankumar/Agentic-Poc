import os
import numpy  as np
from google import genai
from openai import OpenAI
from fastapi import FastAPI
from google.genai import types
from functions.prompts import Greetings
from functions.schema import UserInput, ResponseModel
from functions.config import GEMINI_API_KEY, openai_key
from functions.model_congif import detect_intent_openai, detect_intent_gemini
from functions.helpers import pre_authorization_workflow, handle_pre_authorization

client = genai.Client(api_key=GEMINI_API_KEY)
openclient = OpenAI(api_key=openai_key)

#now i want to add memory to this planner

# ---------- FASTAPI APP ----------
app = FastAPI()

@app.post("/detect_intent", response_model=ResponseModel)
async def detect_intent(user_input: UserInput):
    parsed = detect_intent_openai((user_input.query))
    print(f"llm output is : {parsed}")
    # parsed = detect_intent_gemini((user_input.query))
    Intent, patient_id, payer = parsed.Intent, parsed.patient_id, parsed.payer

    # Logic flow
    if Intent == "other":
        return ResponseModel(
            status="error",
            message="User intent is not related to pre-authorization.",
            Intent=Intent
        )
    elif Intent == "greetings":
        return ResponseModel(
            status="error",
            message=np.random.choice(Greetings),
            Intent=Intent
        )
    elif Intent == "pre_authorization":
        return handle_pre_authorization(Intent, patient_id, payer)