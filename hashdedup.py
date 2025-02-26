#!/usr/bin/python3

from pprint import pprint
from creds import API_KEY, BASE_URL
from functions import immich

prefered_album = "Camera"

headers = {"Accept": "application/json", "x-api-key": API_KEY}


ic = immich(API_KEY, BASE_URL)


albums = ic.get_albums()
album_dict = {}
prefered_dict = {}
for album in albums:
    assets = ic.get_album_assets(album["id"])
    if album["albumName"] == prefered_album:
        for asset in assets:
            prefered_dict[asset["thumbhash"]] = asset

    else:
        album_dict[album["albumName"]] = assets

for album in album_dict:
    for asset in album_dict[album]:
        if asset["thumbhash"] in prefered_dict:
            match = True
            print(f"Possible Duplicate found in {album} and {prefered_album}")
            asset1 = asset
            asset2 = prefered_dict[asset["thumbhash"]]
            fields_to_match = ["thumbhash"]

            for field in fields_to_match:
                if asset1[field] != asset2[field]:
                    match = False
                    print(f"Field {field} does not match")
            exifInfo_to_match = [
                "city",
                "country",
                #"dateTimeOriginal",
                "description",
                "exifImageHeight",
                "exifImageWidth",
                "exposureTime",
                "fNumber",
                #"fileSizeInByte",
                "focalLength",
                "iso",
                #"latitude",
                "lensModel",
                #"longitude",
                "make",
                "model",
                "modifyDate",
                "orientation",
                "projectionType",
                "rating",
                "state",
                "timeZone",
            ]
            for field in exifInfo_to_match:
                if asset1["exifInfo"][field] != asset2["exifInfo"][field]:
                    match = False
                    print(f"Field {field} does not match")
            if match:
                print(f"Deleting {asset1['id']}")
            else:
                print(f"Keeping {asset1['id']} and {asset2['id']}")
                quit()
