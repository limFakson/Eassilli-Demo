import os
import pyrebase
import uuid
from decouple import config

config_file_path = "../../.env"


class FirebaseStorage:
    def __init__(self, file=None, document=None):
        self.file = file
        self.document = document

        # Firebase config for storage
        self.storage_config = {
            "apiKey": config("ApiKey"),
            "authDomain": config("AuthDomain"),
            "projectId": config("ProjectId"),
            "storageBucket": config("StorageBucket"),
            "messagingSenderId": config("SenderId"),
            "appId": config("AppId"),
            "measurementId": config("MeasureId"),
            "databaseURL": config("DatabaseUrl"),
        }

        # Initialise pyrebase to activate storage
        firebase = pyrebase.initialize_app(self.storage_config)
        self.storage = firebase.storage()

    def store_file(self):
        full_filename = self.file.name
        filename, ext = os.path.splitext(full_filename)
        if ext in [".png", ".jpeg", ".jpg", ".svg"]:
            storage_name = f"image/{uuid.uuid4()}{ext}"
        elif ext in [".docs", ".dox", ".pdf", ".txt"]:
            storage_name = f"file/{uuid.uuid1()}{ext}"
        else:
            storage_name = f"media/{uuid.uuid4()}{ext}"

        # Store file in firebase storage
        self.storage.child(storage_name).put(self.file)

        # Storage url from firebase storage
        storage_url = self.storage.child(storage_name).get_url(None)

        return storage_url

    def store_document(self):
        return True
