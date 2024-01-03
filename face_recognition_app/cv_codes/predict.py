import cv2
import numpy as np
import face_recognition
import pickle
from datetime import datetime
import os


# def markAttendance(name, id, dtString):
#     name_id_dt = f"{name},{id},{dtString}"
#     existing_entries = set()
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     csv_path = os.path.join(script_dir, "Attendance.csv")

#     # Read existing entries and add them to a set
#     with open(csv_path, "r") as f:
#         for line in f:
#             entry = line.strip()
#             existing_entries.add(entry)

#     # Check for duplicates
#     if name_id_dt not in existing_entries:
#         # If not a duplicate, write the new entry
#         with open("Attendance.csv", "a") as f:
#             f.write(f"\n{name_id_dt}")


# Load known face encodings, names, and IDs
def enhance_image(img):
    # Apply histogram equalization to enhance image contrast
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    enhanced_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return enhanced_img



def recognize_faces(image_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    encodings_path = os.path.join(script_dir, "encodings.pkl")

    # Load known face encodings and IDs
    with open(encodings_path, "rb") as f:
        data = pickle.load(f)
    encodeListKnown = data["encodings"]
    classNames = data["names"]
    classIDs = data["ids"]
    output = {}
    img = cv2.imread(image_path)

    if img is not None:
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
                output[id] = name

        # Save the image with recognized faces to the same folder
        output_image_name = f"recognized_faces_{os.path.basename(image_path)}"
        output_image_path = os.path.join(os.path.dirname(image_path), output_image_name)
        cv2.imwrite(output_image_path, img)

        return output, output_image_path  # Return the path to the saved image

    else:
        print("Error: Unable to read the loaded image.")
        return None
