import cv2
import numpy as np
import face_recognition
import pickle
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def markAttendance(name, id, dtString):
    name_id_dt = f"{name},{id},{dtString}"
    existing_entries = set()

    # Read existing entries and add them to a set
    with open("Attendance.csv", "r") as f:
        for line in f:
            entry = line.strip()
            existing_entries.add(entry)

    # Check for duplicates
    if name_id_dt not in existing_entries:
        # If not a duplicate, write the new entry
        with open("Attendance.csv", "a") as f:
            f.write(f"\n{name_id_dt}")


def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    root.destroy()
    return file_path


# Load known face encodings and IDs
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)
encodeListKnown = data["encodings"]
classNames = data["names"]
classIDs = data["ids"]

image_file_path = select_image()

if image_file_path:
    img = cv2.imread(image_file_path)

    if img is not None:
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
                y1, x1, y2, x2 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img,
                    f"{name} {id}",
                    (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

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
