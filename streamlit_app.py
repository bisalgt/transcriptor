import streamlit as st
import whisper
import numpy as np
import tempfile
import requests
import deepl
import nltk
import plotly.express as px
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download([
    "stopwords",
    "vader_lexicon",
    "punkt_tab"
])


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

    english_text = get_translation_to_english(result["text"])
    st.text_area(label="English Translation Output", value=english_text)

    sentiment_analyser = SentimentIntensityAnalyzer() # can use pie chart to show it.


    polarity_scores = sentiment_analyser.polarity_scores(english_text)
    
    polarity_scores_df = pd.DataFrame(polarity_scores.items(), columns=["Sentiment", "Score"])
    indx_to_drop = polarity_scores_df[polarity_scores_df["Sentiment"] == "compound"].index
    polarity_scores_df.drop(indx_to_drop, inplace=True)

    fig_piechart = px.pie(polarity_scores_df, values='Score', names='Sentiment', title='Sentiment Analysis of the Audio')

    
    words: list[str] = nltk.word_tokenize(english_text)
    words = [word.lower() for word in words if word.isalpha()]
    fd = nltk.FreqDist(words)
    freq_distribution_df = pd.DataFrame(fd.items(), columns=['used_word', 'count'])
    fig_histogram = px.histogram(freq_distribution_df, x="used_word", y="count", title="Frequency Distribution of Words")

    pie_chart_col, histogram_col = st.columns(2)

    pie_chart_col.plotly_chart(fig_piechart)
    histogram_col.plotly_chart(fig_histogram)