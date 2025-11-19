import src.coll_info
import src.COCO_JSON_gen
import src.UUID_generator
import src.segment_collection_images



dataset_info_path = "dataset_info.md"
images_folder_path = "original_images_test"
output_images_folder = "uuid_images_test"
categories_file = []

collection_info = src.coll_info.extract_collection_info(dataset_info_path)
json_file = src.COCO_JSON_gen.generate_blank_coco_json(
    description=collection_info.get("Description", ""),
    url=collection_info.get("URL", ""),
    version=collection_info.get("Version", ""),
    year=int(collection_info.get("Year", None)),
    contributor=collection_info.get("Contributor", ""),
    date_created=collection_info.get("Date_Created", ""),
    licenses=collection_info.get("Licenses", []),
)
# save json_file to disk
collection_short_name = collection_info.get("Collection_short_name", "")
if collection_short_name:
    json_filename = f"{collection_short_name}.json"
else:
    json_filename = "coco.json"

with open(json_filename, 'w') as f:
    import json
    json.dump(json_file, f, indent=4)
    print(f"Blank COCO JSON file saved as {json_filename}")

uuid_mapping = src.UUID_generator.collection_uuid_generator(images_folder_path, output_images_folder, json_filename=json_filename)

# If file categories_file variable is emptry, add default category object with id 1
if not categories_file:
    with open(json_filename, 'r') as f:
        coco_data = json.load(f)
    coco_data['categories'].append({
        "id": 1,
        "name": "object"
    })
    with open(json_filename, 'w') as f:
        json.dump(coco_data, f, indent=4)
    print("Default category 'object' with id 1 added to COCO JSON file.")
    
src.segment_collection_images.segment_collection_images(output_images_folder, json_filename)