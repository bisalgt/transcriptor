import streamlit as st
import whisper
import numpy as np
import tempfile
import requests
import deepl

# Trying DeepL translation
import deepl

deepl_apikey_filepath = "./notebooks/deepl_apikey.txt"

with open(deepl_apikey_filepath, "r") as rf:
    deepl_apikey = rf.readline() # reading first line which contains apikey

deepl_client = deepl.DeepLClient(deepl_apikey)







def get_translation_to_english(input_text : str) -> str:
    translated_eng_txt = deepl_client.translate_text(input_text, target_lang="EN-US")
    return translated_eng_txt.text

    


audio_file = st.audio_input("Record a voice message")

# requests words to apis and get the meaning
def get_meaning(word: str) -> str:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        definition = data[0]["meanings"][0]["definitions"][0]["definition"]
    else:
        definition = "Word not found."
    return definition




if audio_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_file.read())
        temp_filename = tmp.name

    model = whisper.load_model("base")
    result = model.transcribe(temp_filename)

    # print(result["text"])

    st.text_area(label="Transcript Output", value=result["text"])

    
    st.text_area(label="English Translation Output", value=get_translation_to_english(result["text"]))
    