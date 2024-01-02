import cv2
import numpy as np
import face_recognition
import pickle
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def markAttendance(name, id, dtString):
    with open("Attendance.csv", "r+") as f:
        existing_entries = f.readlines()
        name_id_dt = f"{name},{id},{dtString}\n"
        if name_id_dt not in existing_entries:
            f.write(name_id_dt)

def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    root.destroy()
    return file_path

# Load known face encodings, names, and IDs
def enhance_image(img):
    # Apply histogram equalization to enhance image contrast
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    enhanced_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return enhanced_img

# Load known face encodings, names, and IDs
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)
encodeListKnown = data["encodings"]
classNames = data["names"]
classIDs = data["ids"]

image_file_path = select_image()
if image_file_path:
    img = cv2.imread(image_file_path)
    if img is not None:
        # Enhance the input image
        img = enhance_image(img)

        imgS = cv2.resize(img, (0, 0), None, 1, 1)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex]
                id = classIDs[matchIndex]
                print("Recognized:", name, "ID:", id)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{name}", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                now = datetime.now()
                dtString = now.strftime("%H:%M:%S:%Y-%m-%d")
                markAttendance(name, id, dtString)

        cv2.imshow("Loaded Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Unable to read the loaded image.")
else:
    print("No image file selected.")
