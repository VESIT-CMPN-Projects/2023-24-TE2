import mediapipe as mp
import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow_addons.metrics import MultiLabelConfusionMatrix

with tf.keras.utils.custom_object_scope({'MultiLabelConfusionMatrix': MultiLabelConfusionMatrix}):
    model = load_model("trained_40_88_25c.h5")

def process_and_predict (video_path):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    predictions = []
    Pose = mp_pose.Pose (
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.5)
    
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = Pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            pose = []
            for i, landmark in enumerate(results.pose_landmarks.landmark):
                pose.append([i, landmark.x, landmark.y, landmark.z])
            pose = np.array([pose[:25]])
            pose = pad_sequences(pose, padding='post', dtype='float', truncating='post')
            prediction = model.predict(pose)
            class_pred = np.argmax(prediction)
            predictions.append(class_pred)
        except Exception as e:
            print(e)
            pose = None
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_pose_landmarks_style(),
            )
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return predictions

# process_and_predict("D:\\B. E. CMPN\\Fifth sem\\Mini\\videos\\grow\\grow_33.mp4")