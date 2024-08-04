import json

import google.generativeai as genai


def get_chat_response(user_input, chat_model, application_specific_schema):

    prompt = "Prompt to be evaluated: " + user_input
    gen_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=application_specific_schema,
    )

    raw_response = chat_model.send_message(prompt, generation_config=gen_config)

    response = json.loads(raw_response.text)
    return response
