#!/usr/bin/python3


from creds import API_KEY, BASE_URL, upload_folder
from functions import immich

ic = immich(API_KEY, BASE_URL)


asset_ids = []
album_id = ic.create_album("Google Photos")
hash_db = ic.load_hash_db()


for file in ic.get_image_files(upload_folder):
    file_hash = ic.calculate_image_hash(file)

    if file_hash in hash_db:
        print(f"Skipping {file} - already uploaded")
        continue
    print(f"Uploading {file}")
    asset_id = ic.upload(file)
    ic.add_asset_to_album(asset_id=asset_id, album_id=album_id)
    asset_ids.append(asset_id)
    if asset_id:
        # Save hash after successful upload
        hash_db[file_hash] = asset_id
        ic.save_hash_db(hash_db)

ic.add_asset_to_album(asset_id=asset_ids, album_id=album_id)
