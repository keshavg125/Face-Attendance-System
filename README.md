# **Face Attendance System with Real-Time Database**

## **Description**
The **Face Attendance System** is a real-time face recognition application designed to track attendance based on facial recognition technology. It uses **OpenCV** and **Appwrite** for face detection, recognition, and real-time attendance logging. The system logs attendance securely, ensuring seamless management of student or employee attendance records.

### **Key Features:**
- **Face Detection & Recognition**: Uses OpenCV and dlib for detecting and recognizing faces.
- **Real-Time Attendance Logging**: Saves attendance data to Appwrite for secure storage and retrieval.
- **User-Friendly Interface**: Provides a simple and intuitive UI to manage attendance and settings.

## **Files in this Repository**

- **EncodeFile.p**: This file contains encoded facial features used to compare and recognize faces during the attendance process.
- **EncodeGenerator.py**: A script that generates the encoded facial features from input images and saves them to **EncodeFile.p**.
- **Images.zip**: A zip file containing sample images of users for facial recognition training and testing.
- **Resources.zip**: Contains background images and different image modes, such as:
  - **Active images**: Background images used for real-time attendance.
  - **Marked images**: Images that are already used to mark attendance.
- **appwrite_test.py**: A script for testing Appwrite integration with the system (optional for extended functionalities like user management).
- **main.py**: The main script that runs the face attendance system, handles face recognition, and logs the attendance in real-time.

### **Requirements:**
To run this project, you will need the following dependencies:

- **Python**
- **OpenCV**
- **dlib**
- **Appwrite SDK**
