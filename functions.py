import requests
import requests
import os
from datetime import datetime
from pprint import pprint
import json
import hashlib


class immich:
    def __init__(self, api_key, base_url):
        self.headers = {"Accept": "application/json", "x-api-key": api_key}
        self.base_url = base_url

    def get_duplicates(self):
        response = requests.get(f"{self.base_url}/duplicates", headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_albums(self):
        response = requests.get(f"{self.base_url}/albums", headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_album_assets(self, album_id):
        response = requests.get(
            f"{self.base_url}/albums/{album_id}", headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["assets"]

    def set_asset_description(self, asset_id, description):
        response = requests.put(
            f"{self.base_url}/assets/{asset_id}",
            headers=self.headers,
            json={"description": description},
        )
        if response.status_code == 200:
            return True
        else:
            print(response.json())
            return False

    def delete_asset(self, asset_id):
        payload = {"force": False, "ids": [asset_id]}
        response = requests.delete(
            f"{self.base_url}/assets",
            headers=self.headers,
            json=payload,
        )
        if response.status_code == 200:
            return response.json()

    def calculate_image_hash(self, file_path):
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def load_hash_db(self, db_path="image_hashes.json"):
        if os.path.exists(db_path):
            with open(db_path, "r") as f:
                return json.load(f)
        return {}

    def save_hash_db(self, hash_db, db_path="image_hashes.json"):
        with open(db_path, "w") as f:
            json.dump(hash_db, f)

    def create_album(self, name):
        payload = {
            "albumName": name,
            "albumUsers": [],
            "assetIds": [],
            "description": "Description",
        }
        albums = requests.get(f"{self.base_url}/albums", headers=self.headers).json()
        for album in albums:
            if album["albumName"] == name:
                print("Album already exists")
                return album["id"]
        response = requests.post(
            f"{self.base_url}/albums", headers=self.headers, json=payload
        )
        print("Album created")
        return response.json()["id"]

    def upload(self, file):
        stats = os.stat(file)

        data = {
            "deviceAssetId": f"{file}-{stats.st_mtime}",
            "deviceId": "python",
            "fileCreatedAt": datetime.fromtimestamp(stats.st_mtime),
            "fileModifiedAt": datetime.fromtimestamp(stats.st_mtime),
            "isFavorite": "false",
        }

        files = {"assetData": open(file, "rb")}

        response = requests.post(
            f"{self.base_url}/assets", headers=self.headers, data=data, files=files
        )
        if response.status_code not in [200, 201]:
            print(response.text)
            print(response.status_code)
        response = response.json()
        if response["status"] == "created":
            print("Asset uploaded")
            return response["id"]
        elif response["status"] == "duplicate":
            print("Asset already exists")
            return response["id"]
        else:
            pprint(response)
            quit()

    def add_asset_to_album(self, asset_id=None, album_id=None):
        if isinstance(asset_id, list):
            payload = {"ids": asset_id}
        else:
            payload = {"ids": [asset_id]}
        response = requests.put(
            f"{self.base_url}/albums/{album_id}/assets",
            headers=self.headers,
            json=payload,
        )
        if response.status_code == 200:
            print("Asset added to album")

    def get_image_files(self, directory):
        """Recursively get all image files from directory and subdirectories"""
        image_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".webp",
            ".mp4",
            ".mov",
        )
        image_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_files.append(os.path.join(root, file))

        return image_files
