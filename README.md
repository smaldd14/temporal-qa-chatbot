# temporal-qa-chatbot

## Requirements
`pip install openai pinecone-client streamlit langchain dotenv selenium html2text`

## Introduction
`app.py` is a streamlit app that can user's can use to chat with [TemporalIO's Java Documentation](https://docs.temporal.io/dev-guide/java)

Run with `streamlit run app.py`

`common.py` contains common functions used by the other scripts.

`download-docs.py` is a script that downloads the documentation from the website and saves it to a local directory.

`chunk-docs.py` is a script that chunks the documentation into smaller pieces. This is used to create the pinecone index.

`embed-docs.py` is a script that creates embeddings for each chunk of documentation and saves it to a pinecone index.
