import cv2
import os
import numpy as np
import face_recognition
import pickle

def extract_frames(video_path, output_folder, frame_rate=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / frame_rate)

    count = 0
    success, frame = video_capture.read()
    while success:
        if count % frame_interval == 0:
            frame_file = os.path.join(output_folder, f"frame{count}.jpg")
            cv2.imwrite(frame_file, frame)
        success, frame = video_capture.read()
        count += 1

    video_capture.release()

def load_images_from_folder(folder):
    images = []
    classNames = []
    classIDs = []

    for person_folder in os.listdir(folder):
        person_path = os.path.join(folder, person_folder)
        if os.path.isdir(person_path):
            person_images = []
            for file in os.listdir(person_path):
                file_path = os.path.join(person_path, file)
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    img = cv2.imread(file_path)
                    if img is not None:
                        person_images.append(img)
                elif file.endswith(('.mp4', '.avi', '.mov')):
                    extract_frames(file_path, person_path)

            if person_images:
                images.append(person_images)
                name, id = person_folder.rsplit('_', 1)  # Split name and ID
                classNames.append(name)
                classIDs.append(id)

    return images, classNames, classIDs

def findEncodings(images):
    encodeList = []
    for person_images in images:
        person_encodings = []
        for img in person_images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)
            if len(encode) > 0:
                person_encodings.append(encode[0])
        if person_encodings:
            average_encoding = np.mean(person_encodings, axis=0)
            encodeList.append(average_encoding)
        else:
            encodeList.append(None)
    return encodeList

path = 'Video_Attendance'
images, classNames, classIDs = load_images_from_folder(path)
encodeListKnown = findEncodings(images)
print('Encoding Complete')

with open('encodings.pkl', 'wb') as f:
    pickle.dump({"encodings": encodeListKnown, "names": classNames, "ids": classIDs}, f)

print("Encodings, names, and IDs saved to encodings.pkl")
