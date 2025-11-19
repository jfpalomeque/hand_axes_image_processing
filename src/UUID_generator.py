"""
This module provides functionality to generate UUIDs (Universally Unique Identifiers), for each
image in the dataset, plus for each individual object within those images.
Said UUIDs will be saved in the metadata files associated with the images and objects and
on the EXIF data of the image files.
Image file names will also be renamed to include the image UUID.
To avoid unintended changes to the original images, modified images will be saved as copies in a
separate directory.
"""
import uuid
import os
import shutil
import piexif
import piexif.helper
import json
from PIL import Image

def generate_uuid(images_folder_path):
    """
    Generates UUIDs for each image and object in the dataset.
    
    Args:
        images_folder_path (str): Path to the folder containing images.
        
    Returns:
        dict: A dictionary mapping image file names to their UUIDs and object UUIDs.        
    """
    
    
    uuid_mapping = {}
    
    for image_file in os.listdir(images_folder_path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_uuid = str(uuid.uuid4())
            uuid_mapping[image_file] = {
                "original_file_name": image_file,
                "original_file_path": os.path.join(images_folder_path, image_file),
                "image_uuid": image_uuid
            }
    return uuid_mapping

def copy_uuid_images(uuid_mapping, output_images_folder, json_filename):
    """
    Creates a copy of images with UUIDs in their filenames.
    Adds the image UUID to the EXIF data of the copied images.
    
    Args:
        uuid_mapping (dict): The UUID mapping dictionary.
        output_images_folder (str): Path to the output folder where the mapping will be saved.
    """
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    total_images = len(uuid_mapping)
    
    for n, image_file in enumerate(uuid_mapping, start=1):
        image_uuid = uuid_mapping[image_file]["image_uuid"]
        original_image_name = uuid_mapping[image_file]["original_file_name"]
        file_extension = os.path.splitext(image_file)[1]
        new_image_file_name = f"{image_uuid}{file_extension}"
        uuid_mapping[image_file]["image_uuid_file_name"] = new_image_file_name
        new_image_file_path = os.path.join(output_images_folder, new_image_file_name)
        shutil.copy2(uuid_mapping[image_file]["original_file_path"], new_image_file_path)
        # Add UUID to EXIF data
        exif_dict = piexif.load(new_image_file_path)
        user_comment = f"{image_uuid}"
        exif_dict['Exif'][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(user_comment, encoding="unicode")
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, new_image_file_path)
        # Get image size using pillow
        
        with Image.open(new_image_file_path) as img:
            width, height = img.size
        print(f"Copied and updated EXIF for image: {original_image_name} {new_image_file_name}. Image {n} of {total_images}.")
        
        # Add image details to the coco json file
        with open(json_filename, 'r') as f:
            coco_data = json.load(f)
        image_info = {
            "id": image_uuid,
            "file_name": new_image_file_name,
            "width": width,
            "height": height
        }
        coco_data['images'].append(image_info)
        with open(json_filename, 'w') as f:
            json.dump(coco_data, f, indent=4)
    
    # save the mapping to a csv file for reference on the main directory
    mapping_file_path = os.path.join(output_images_folder, "uuid_mapping.csv")

    with open(mapping_file_path, 'w') as f:
        f.write("original_file_name,original_file_path,image_uuid,image_uuid_file_name\n")
        for image_file, uuids in uuid_mapping.items():
            f.write(f"{uuids['original_file_name']},{uuids['original_file_path']},{uuids['image_uuid']},{uuids['image_uuid_file_name']}\n")
        print("All images copied with UUIDs in filenames and EXIF data updated.")


def collection_uuid_generator(images_folder_path, output_images_folder, json_filename):
    """
    Main function to generate UUIDs for images and copy them with updated filenames and EXIF data.
    
    Args:
        images_folder_path (str): Path to the folder containing images.
        output_images_folder (str): Path to the output folder where the mapping will be saved.
    """
    uuid_mapping = generate_uuid(images_folder_path)
    copy_uuid_images(uuid_mapping, output_images_folder, json_filename)
    return uuid_mapping