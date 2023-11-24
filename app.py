import streamlit as st
import pickle
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# load the model and tokenizer
model = tf.keras.models.load_model('model.h5')
tokenizer = pickle.load(open('tokenizer.pickle', 'rb'))

# add title
st.title('Hoax Detector App')
st.write('Periksa kebenaran berita politik, stop sebarkan informasi tak bertanggungjawab!')

# add form for input text
form = st.form(key='teks-berita')
user_input = form.text_area('Masukkan teks berita disini')
predict = form.form_submit_button('Prediksi')

# process input news
def clean_input(text):
    #remove html
    html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    text = re.sub(html, "", text)

    #remove_non_ascii characters
    text = re.sub(r'[^\x00-\x7f]',r'', text)

    # remove_special_characters
    emoji_pattern = re.compile(
        '['
        u'\U0001F600-\U0001F64F'  # emoticons
        u'\U0001F300-\U0001F5FF'  # symbols & pictographs
        u'\U0001F680-\U0001F6FF'  # transport & map symbols
        u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
        u'\U00002702-\U000027B0'
        u'\U000024C2-\U0001F251'
        ']+',
        flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # remove_punct
    text = re.sub(r'[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+', "", text)
    
    # lowercase text
    text = text.lower()

    return text

# making prediction
def predict(model, user_input):
    # clean the input_news
    text = clean_input(user_input)
    # tokenize the news
    text_sequences = tokenizer.texts_to_sequences([text])
    text_padded = pad_sequences(text_sequences, maxlen=1313, padding='post', truncating='post')
    # prediction
    tresh = 0.55
    proba = model.predict(text_padded)
    class_id = int((proba > tresh).astype(int)[0][0])
    # map integer class ID to string
    class_label = 'FAKTA' if class_id == 0 else 'HOAX'
    # calculate the probability in each class
    prob_hoax = round(float(proba[0][0])*100,2)
    prob_valid = round((100 - prob_hoax),2)
    # show the result
    if class_label == 'HOAX':
        return st.error(f"Ini berita hoax dengan tingkat kebenaran sebesar: {prob_hoax}%", icon="🚨")
    else:
        return st.success(f"Ini berita valid dengan tingkat kebenaran sebesar: {prob_valid}%")
    
# only predict if text is not null
if user_input != '':
    predict(model, user_input)