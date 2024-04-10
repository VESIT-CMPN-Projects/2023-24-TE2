import google.generativeai as genai
import os
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-pro")

def get_sentence(words):
    prompt = "You are a sign language translator. You are being given a set of words collected from people using sign language, the words are what sentence they want to speak. Generate a grammatically correct and meaningful sentence using those words. Do not add context to the sentence. Return only the sentence and nothing more. \nWords: " + ', '.join(words) + "."
    response = model.generate_content(
        prompt,
    )
    return response.text

def translate_sentence(sentence, language):
    translator = Translator()
    return translator.translate(sentence, dest=language).text

def speak(sentence, language):
    gtts = gTTS(sentence, lang=language)
    gtts.save("temp\\output.mp3")
    playsound("temp\\output.mp3")
    os.remove("temp\\output.mp3")
    return