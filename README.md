# Hoax Detector App

Are you looking for a place to validate whether an Indonesian political news is hoax or valid? You go to the right place. Just paste your Indonesian Political Text News in the text box, wait a second, and boom the prediction result come out.

## Setup environment
```
conda create --name hoax-detection-app python=3.9
conda activate hoax-detection-ap
pip install streamlit pickle-mixin scikit-learn tensorflow emoji regex
```

## Run streamlit app
```
streamlit run app.py
```

## The dashboard appearence

It has been deployed, [let's playing around with it](https://hoax-political-news-detection.streamlit.app/)