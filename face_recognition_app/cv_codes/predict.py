import cv2
import numpy as np
import face_recognition
import pickle
from datetime import datetime
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
                cv2.putText(
                    img,
                    f"{name}",
                    (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )
                output[id] = name
                now = datetime.now()
                dtString = now.strftime("%H:%M:%S:%Y-%m-%d")
                # markAttendance(name, id, dtString)

        cv2.imshow("Loaded Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Unable to read the loaded image.")
else:
    print("No image file selected.")
