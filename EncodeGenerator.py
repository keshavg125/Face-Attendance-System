import cv2
import face_recognition
import pickle
import os
from appwrite.client import Client
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage

# Initialize Appwrite Client
client = Client().set_endpoint("https://cloud.appwrite.io/v1") \
                 .set_project("67d9add00021069d93a0") \
                 .set_key("standard_95ea51d7c12949e551c380b3ef542d14084695d59ee65b1b59d66fa737373708b7609c4cafdc6dec186f3128636439aa40760983c98d625789ac89998b1137afb3fd6e5728262463604677b82acce59669bfab3d6863c6e891f41b1a98cc094787faa07c348cb668134990c78c2283e3785a70b08bcc499642f29eb9bd68bbf1")
storage = Storage(client)
BUCKET_ID = "67d9ae060012dafa4cad"

# IMPORTING STUDENT IMAGES
folderPath = 'Images'
pathList = os.listdir(folderPath) # Name of images
imgList = []
studentIDs = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIDs.append(os.path.splitext(path)[0])

    #UPOADING IMAGES TO STORAGE
    try:
        response = storage.create_file(BUCKET_ID, "unique()", InputFile.from_path(os.path.join(folderPath, path)))
        print(f"✅ Uploaded: {path}")
    except Exception as e:
         print(f"❌ Error uploading {path}: {e}")

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started.......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWthIDs = [encodeListKnown,studentIDs]
print("Encoding Complete.......")

# PICKLE FILE
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWthIDs,file)
file.close()
print("File Saved.......")