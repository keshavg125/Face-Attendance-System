from appwrite.client import Client
from appwrite.services.databases import Databases

# Initialize Appwrite Client
client = Client().set_endpoint("https://cloud.appwrite.io/v1") \
                 .set_project("67d9add00021069d93a0") \
                 .set_key("standard_95ea51d7c12949e551c380b3ef542d14084695d59ee65b1b59d66fa737373708b7609c4cafdc6dec186f3128636439aa40760983c98d625789ac89998b1137afb3fd6e5728262463604677b82acce59669bfab3d6863c6e891f41b1a98cc094787faa07c348cb668134990c78c2283e3785a70b08bcc499642f29eb9bd68bbf1")

database = Databases(client)

DATABASE_ID = "67d9adf1001ab20c1d0e"
COLLECTION_ID = "67d9b7170018fab02511"

# Student Data
students_data = {
    "321654": {
        "name": "Murtaza Hassan",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 7,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "852741": {
        "name": "Emly Blunt",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "963852": {
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}

# Insert Data into Database
for student_id, data in students_data.items():
    database.update_document(DATABASE_ID, COLLECTION_ID, student_id, data)
    # print(f"✅ Added Student {student_id}")
