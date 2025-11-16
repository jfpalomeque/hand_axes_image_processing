"""
This module generates a blank COCO JSON compatible file structure.
A function will get general information about the dataset and populate the relevant fields.
The generated JSON file will then be used and populated by other modules in the pipeline.
"""

def generate_blank_coco_json(
    description="",
    url="",
    version="",
    year=None,
    contributor="",
    date_created="",
    licenses=[],
):
    blank_coco_json = {
        "info": {
            "description": description,
            "url": url,
            "version": version,
            "year": year,
            "contributor": contributor,
            "date_created": date_created
        },
        "licenses": licenses,
        "images": [],
        "annotations": [],
        "categories": []
    }
    return blank_coco_json