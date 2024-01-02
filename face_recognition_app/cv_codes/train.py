import os
import numpy as np
import face_recognition
import cv2
import pickle

def extract_frames(video_path, output_folder, max_frames=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        raise Exception(f"Unable to open video file: {video_path}")

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / 5)  # Adjust the frame rate here
    count, face_count = 0, 0

    success, frame = video_capture.read()
    while success and face_count < max_frames:
        if count % frame_interval == 0:
            temp_frame = frame.copy()
            temp_frame_rgb = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB)
            if face_recognition.face_locations(temp_frame_rgb):
                frame_file = os.path.join(output_folder, f"frame{face_count + 1}.jpg")
                cv2.imwrite(frame_file, temp_frame)
                face_count += 1

        success, frame = video_capture.read()
        count += 1

    video_capture.release()
    print(f"Frames extracted from {video_path}")

def enhance_image(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    enhanced_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return enhanced_img

def load_images_from_folder(folder):
    images, classNames, classIDs = [], [], []
    for person_folder in os.listdir(folder):
        person_path = os.path.join(folder, person_folder)
        if os.path.isdir(person_path):
            person_images = []
            for file in os.listdir(person_path):
                file_path = os.path.join(person_path, file)
                if file.endswith(('.jpg', '.jpeg', '.png')):
                    img = cv2.imread(file_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        enhanced_img = enhance_image(img)
                        person_images.append(enhanced_img)
                elif file.endswith(('.mp4', '.avi', '.mov')):
                    extract_frames(file_path, person_path)

            if person_images:
                images.append(person_images)
                name, id = person_folder.rsplit('_', 1)
                classNames.append(name)
                classIDs.append(id)

    return images, classNames, classIDs

model_path = "dlib_face_recognition_resnet_model_v1.dat"

def findEncodings(images):
    encodeList = []
    for person_images in images:
        person_encodings = []
        for img in person_images:
            face_locations = face_recognition.face_locations(img)
            face_encodings = face_recognition.face_encodings(img, face_locations, model=model_path)
            if face_encodings:
                average_encoding = np.mean(face_encodings, axis=0)
                person_encodings.append(average_encoding)
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
