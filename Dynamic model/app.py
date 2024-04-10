import streamlit as st
from process_video import process_and_predict
from helper import get_sentence, translate_sentence, speak
import os
from scipy import stats

# Fetch classes from dynamic.names
with open('dynamic.names', 'r') as file:
    classes = file.readlines()
    classes = [c.strip() for c in classes]

# Function to process a video
def process_single_video(video_file):
    video_path = os.path.join("temp", video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())
    predictions = process_and_predict(video_path)
    os.remove(video_path)
    return predictions

def get_word(predictions):
    print(predictions)
    word = "None"
    if predictions is not None:
        final_prediction = stats.mode(predictions)
        word = classes[final_prediction[0]]
    return word

# Function to generate sentence from words
def generate_sentence(words, language):
    sentence = get_sentence(words)
    if language == "English":
        return sentence
    else:
        return translate_sentence(sentence, language)

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Marathi": "mr"
}

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="Sign Language Translation", 
        layout="centered", 
        initial_sidebar_state="collapsed"
    )
    st.header("Sign Language Translation")
    
    # Choose language
    language = language_codes[st.selectbox("Choose language", list(language_codes.keys()))]

    # Upload videos
    uploaded_files = st.file_uploader("Upload your video(s)", accept_multiple_files=True)

    # Process videos sequentially
    if st.button("Process Videos"):
        words = []
        with st.spinner("Processing videos..."):
            if uploaded_files:
                for video_file in uploaded_files:
                    pose = process_single_video(video_file)
                    word = get_word(pose)
                    words.append(word)
                st.write("Pose extraction completed for all videos.")
                
        with st.spinner("Generating sentence..."):
            try:
                sentence = generate_sentence(words, language)
                st.write(sentence)
                speak(sentence, language)
            except Exception as e:
                st.error("An error occurred while generating the sentence.")
                st.error(e)

if __name__ == "__main__":
    main()