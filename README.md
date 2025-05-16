# transcriptor

## Step 1. Streamlit app to visualize transcript  and translation

- OpenAI whisper model used for Transcription
- DeepL API used for Translation to English
- The output shown using Streamlit App
- nltk used for Sentiment Analysis
- plotly chart created and plotted on streamlit interface

![Output](./outputs/Audio%20transcription%20and%20analysis%20with%20nltk.png)


### Todo :
- Integrate Free Dictionary API to see the word meaning in english when hover over to the texts.



### How to Run

1. Experimented with Python 3.11 Version
2. Pull the package to local machine, go inside the root folder and create a virtual environment using `python -m venv env_name`
3. Activate the virtual machine and install required packages `pip install -r requirements.txt`
4. Make sure to have a file called `deepl_apikey.txt` which contains the apikey (Can be generated free from DeepL website with limited tokens translation per month)
5. Run in terminal `streamlit run streamlit_app.py`
6. This will open browser. Record audio in the browser and you will receive output on the streamlit app/webpage.
