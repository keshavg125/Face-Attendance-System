import os
import cv2
import pickle
import cvzone
import numpy as np
import face_recognition
from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage
from appwrite_test import database

# Initialize Appwrite Client
client = Client().set_endpoint("https://cloud.appwrite.io/v1") \
                 .set_project("67d9add00021069d93a0") \
                 .set_key("standard_95ea51d7c12949e551c380b3ef542d14084695d59ee65b1b59d66fa737373708b7609c4cafdc6dec186f3128636439aa40760983c98d625789ac89998b1137afb3fd6e5728262463604677b82acce59669bfab3d6863c6e891f41b1a98cc094787faa07c348cb668134990c78c2283e3785a70b08bcc499642f29eb9bd68bbf1")
storage = Storage(client)
BUCKET_ID = "67d9ae060012dafa4cad"

# WEB-CAM-ON
cap = cv2.VideoCapture(0)
cap.set(4, 480) # HEIGHT
cap.set(3, 640) # WIDTH

imgBg = cv2.imread('Resources/background.png')

# IMPORTING IMAGES MODE
folderMode = 'Resources/Modes'
modePathList = os.listdir(folderMode) # Name of images
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderMode,path)))


# LOAD ENCODING FILE
print("Loading encode file.......")
file = open('EncodeFile.p', 'rb')
encodeListKnownWthIDs = pickle.load(file)
file.close()
encodeListKnown,studentIDs = encodeListKnownWthIDs
print("Encode file loaded.......")

modeType = 0
counter = 0
idd = -1

# SHOWING WEB-CAM
while True:
    success, img = cap.read()

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,faceCurFrame)

    imgBg[162 : 162+480 , 55 : 55+640] = img
    imgBg[44 : 44+633 , 808 : 808+414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(matches)
        # print(faceDist)

        matchIndex = np.argmin(faceDist)

        # print("known face detected")
        if matches[matchIndex]:
            # Rectangle Around The Face || x y width height
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 =y1*4, x2*4, y2*4, x1*4
            bbox = x1+55, y1+162, x2-x1, y2-y1
            imgBg = cvzone.cornerRect(imgBg, bbox, rt = 0)

            idd = studentIDs[matchIndex]
            # print(idd)

            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:

        if counter == 1:
            # Fetch Student Data from Appwrite Database
            studentInfo = database.get_document(
                database_id = "67d9adf1001ab20c1d0e",
                collection_id = "67d9b7170018fab02511",
                document_id = idd
            )
            # print(studentInfo)

            # Get the list of all files in the storage bucket
            files = storage.list_files("67d9ae060012dafa4cad")
            # Find the file ID for the given student ID (idd)
            file_id = next((file["$id"] for file in files["files"] if file["name"] == f"{idd}.png"), None)
            if file_id:
                # Download and decode the image
                file = storage.get_file_download("67d9ae060012dafa4cad", file_id)
                array = np.frombuffer(file, np.uint8)
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

        cv2.putText(imgBg, str(studentInfo['total_attendance']), (861, 125),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBg, str(studentInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBg, str(idd), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBg, str(studentInfo['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBg, str(studentInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBg, str(studentInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBg, str(studentInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBg[175:175 + 216, 909:909 + 216] = imgStudent






    # cv2.imshow("Webcam", img)
    cv2.imshow("Face-Attendance", imgBg)
    cv2.waitKey(2)