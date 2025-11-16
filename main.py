import src.coll_info
import src.COCO_JSON_gen
import src.UUID_generator



dataset_info_path = "dataset_info.md"
images_folder_path = "original_images"
output_images_folder = "uuid_images"

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
print(json_file)

uuid_mapping = src.UUID_generator.collection_uuid_generator(images_folder_path, output_images_folder)