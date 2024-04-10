import tensorflow as tf
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from process_video import process_and_predict
from helper import get_sentence
from tensorflow_addons.metrics import MultiLabelConfusionMatrix

with tf.keras.utils.custom_object_scope({'MultiLabelConfusionMatrix': MultiLabelConfusionMatrix}):
    model = load_model("trained_26_89_25c.h5")

# fetch classes from dynamic.names
with open('dynamic.names', 'r') as file:
    classes = file.readlines()
    classes = [c.strip() for c in classes]

print("\nPlease choose your language: ")
language = input("\n1. English\n2. Hindi")

videos = int(input("\nHow many videos do you want to process? "))
words = []

for i in range(videos):
    video_path = input("\nEnter the path of the video: ")
    processed = process_and_predict(video_path)
    if processed is not None:
        processed = pad_sequences(processed, padding='post', dtype='float', truncating='post')
        prediction = model.predict(processed)
        class_pred = np.argmax(prediction)
        class_pred = np.array([class_pred])
        words.append(classes[class_pred[0]])

print("\nGenerating sentences...")
sentence = get_sentence(words)
print("\nGenerated sentence:", sentence)