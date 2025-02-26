#!/usr/bin/python3

from pprint import pprint
from creds import API_KEY, BASE_URL
from functions import immich

delete_album = "Google Photos"

ic = immich(API_KEY, BASE_URL)


albums = ic.get_albums()
album_dict = {}
for album in albums:
    x = []
    assets = ic.get_album_assets(album["id"])
    for asset in assets:
        x.append(asset["id"])
    album_dict[album["albumName"]] = x

duplicate_counter = 0
duplicates = ic.get_duplicates()
for duplicate in duplicates:
    match = True
    if len(duplicate["assets"]) == 2:
        asset1 = duplicate["assets"][0]
        asset2 = duplicate["assets"][1]

        # if (
        #    asset1["id"] == "4c4ed8fb-1223-4955-962a-ea89a8f9f079"
        #    or asset2["id"] == "4c4ed8fb-1223-4955-962a-ea89a8f9f079"
        # ):
        #    pprint(asset1)
        #    pprint(asset2)
        #    quit()

        # fields_to_match = ["fileCreatedAt", "localDateTime", "thumbhash"]
        fields_to_match = ["thumbhash"]
        for field in fields_to_match:
            if asset1[field] != asset2[field]:
                match = False
                # print(f"Field {field} does not match")
        if match:
            exifInfo_to_match = [
                "city",
                "country",
                "dateTimeOriginal",
                #"description",
                "exifImageHeight",
                "exifImageWidth",
                "exposureTime",
                "fNumber",
                # "fileSizeInByte",
                "focalLength",
                "iso",
                "lensModel",
                # "latitude",
                # "longitude",
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
                size1 = asset1["exifInfo"]["fileSizeInByte"]
                size2 = asset2["exifInfo"]["fileSizeInByte"]
                if size1 != size2:
                    if size1 > size2:
                        difference = size1 - size2
                    else:
                        difference = size2 - size1
                    if difference > 5:
                        print("Difference too big")
                        match = False
            if match:
                duplicate_counter += 1
                album_match = 0
                if asset1["id"] in album_dict[delete_album]:
                    delete_id = asset1["id"]
                    keep_id = asset2["id"]
                    album_match += 1
                if asset2["id"] in album_dict[delete_album]:
                    delete_id = asset2["id"]
                    keep_id = asset1["id"]
                    album_match += 1

                if album_match == 1:
                    if ic.set_asset_description(delete_id, f"Duplicate of {keep_id}"):
                        print(f"Deleted {delete_id}")
                        ic.delete_asset(delete_id)
                elif album_match == 2:
                    print("Both in delete album")
                elif album_match == 0:
                    print("No album match")
pprint(f"Deleted {duplicate_counter} duplicates")
