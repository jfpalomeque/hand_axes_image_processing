import src.segment_unique_object as suo
import os
import json
from pycocotools import mask as maskutils
import numpy as np

def segment_collection_images(folder_path, coco_json_file):
    """
    Segment multiple images in a folder, assuming each image contains a single object on a black background.
    Returns a dictionary mapping image filenames to their masks and bounding boxes.
    """
    n_files = len(os.listdir(folder_path))
    print(f"Segmenting {n_files} images in folder: {folder_path}")
    
    for i, filename in enumerate(os.listdir(folder_path)):
        print(f"Processing image {i+1}/{n_files}: {filename}")
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            uuid = filename.split('.')[0]
            img_path = os.path.join(folder_path, filename)
            mask, bbox = suo.segment_unique_object(img_path)
            
            # Encode mask to COCO RLE
            rle = maskutils.encode(np.asfortranarray(mask.astype(np.uint8)))
            rle["counts"] = rle["counts"].decode("ascii")  # JSON-serialisable
            
            # Save mask and bbox to COCO JSON as annotation
            with open(coco_json_file, 'r') as f:
                coco_data = json.load(f)
            
            coco_data['annotations'].append({
                'id': f'{uuid}_ann',
                'image_id': uuid,
                'bbox': bbox,
                'segmentation': rle,
                'category_id': 1  
                
            })
            
            with open(coco_json_file, 'w') as f:
                json.dump(coco_data, f, indent=4)
            
            
    return None
