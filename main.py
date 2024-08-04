import contextvars

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from Connection import setup_connection, get_context_var
from model import get_chat_response
import google.generativeai as genai
import os

user_context = contextvars.ContextVar('user_context', default={})
load_dotenv()

def configure_genai():
    GOOGLE_API_KEY=os.environ['API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)


class FreeTextRequestObject(BaseModel):
    free_text: str
    token: str


class ConnectionRequestObject(BaseModel):
    product_code: str


app = FastAPI()

configure_genai()
model = genai.GenerativeModel('gemini-1.5-pro')


def setup_model(token, context):
    print("\nDefault temperature: " + str(genai.get_model('models/gemini-1.5-pro').temperature))
    print("\nDefault top_k: " + str(genai.get_model('models/gemini-1.5-pro').top_k))
    print("\nDefault top_p: " + str(genai.get_model('models/gemini-1.5-pro').top_p))
    print("\nMax output tokens: " + str(genai.get_model('models/gemini-1.5-pro').output_token_limit))
    chat = model.start_chat(history=[])
    context_vars = user_context.get()
    context_vars[token] = {'chat':  chat, 'app_schema': context["app_schema"]}
    full_context = context["generic_context"] + context["app_context"]
    chat.send_message(full_context)


@app.post("/establishConnection")
def establish_connection(req: ConnectionRequestObject):
    try:
        response = setup_connection(req.product_code)
        if response["status_code"] == 200:
            setup_model(response["token"], response["context"])
            return JSONResponse(content={"token": response["token"]}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Product code not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/getJsonFromFreeText")
def parse_free_text_to_json(req: FreeTextRequestObject):
    try:
        context_var = get_context_var(req.token, user_context)
        response = get_chat_response(req.free_text, context_var["chat"], context_var["app_schema"])
        print("\n-------------------------------------------------------------------------------------------")
        print(context_var["chat"].history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Invalid token"))