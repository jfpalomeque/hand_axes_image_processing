# Hand-axes Image Processing & COCO Generator pipeline

This repository shows a technical demo of an automaic pipeline to prepare and process image collections of archaeological artifacts for computer vision workflows. Specifically, it was initially developed to work with the Lower Palaeolithic hand-axes / bifaces dataset from the Archaeology Data Service (ADS), when bulk downloading the images and data as explained in this other [repository](https://github.com/jfpalomeque/hand_axes_database_downloader).

 The primary goals are:

- Generate a COCO-format JSON (blank or partially populated) for the collection.
- Convert image filenames to UUID-based names while producing a mapping file.
- Run an image segmentation pipeline over a collection and embed annotations into the COCO JSON.

The code is lightweight and intended for researchers who want to convert archaeological image collections into formats suitable for machine learning / computer vision experiments.

## Image format and structure
This pipeline assumes that the original images are stored in a folder named `original_images/`. The images should be in standard formats such as JPEG or PNG. The output UUID-named images will be saved in a folder named `uuid_images/`.
A file called dataset_info.md is used to provide collection metadata (title, year, contributor, etc.) that will be embedded into the COCO JSON header.

The development was done using the mentioned ADS bifaces dataset. In this dataset, images are in JPEG format, with only one artifact per image, typically centered against a plain background. Some information and a graphic scale are included in the superior part of the image.

## How to use it
- Clone this repository.
- Install required dependencies using `pip install -r requirements.txt`.
- Fill in the `dataset_info.md` file with your collection metadata.
- Place your original images in the `original_images/` folder.
- Run the main script: `python main.py`.


### What `main.py` does (default behaviour):

- Reads collection metadata from `dataset_info.md`.
- Generates a blank COCO JSON (uses collection metadata for description, contributor, year, etc.) and saves it as `<collection_short_name>.json` (or `coco.json`).
- Converts images found in `original_images_test/` into UUID-named copies in `uuid_images_test/` and writes a UUID mapping CSV.
- Ensures at least one default category exists in the COCO JSON (id=1, name="object").
- Runs the segmentation pipeline in `src/segment_collection_images.py` to populate image/annotation entries.

Adjust the paths inside `main.py` (or copy/extend it) to work with your own `original_images/` folder and desired output locations.

## Outputs
- A COCO-format JSON file with collection metadata, image entries, and segmentation annotations.
- A folder with UUID-named copies of the original images.
- A CSV mapping original filenames to UUID filenames in directory `uuid_images/`.

## Why this repo?

This repository aims to facilitate the automatic preparation of large archaeological image datasets for computer vision tasks. The use of UUIDs allows the combination of multiple datasets avoiding filename collisions. Using the ADS bifaces dataset as a case study, this pipeline was able to process 10,668 images.


## 📚 Citation of the original images dataset

If you use the mentioned ADS bifaces data included or referenced here, please cite the original source:

**Lower Palaeolithic technology, raw material and population ecology (bifaces)**
*Gilbert Marshall, David Dupplaw, Derek Roe, Clive Gamble (2002)*
DOI: [10.5284/1000354](https://doi.org/10.5284/1000354)

## ⚠️ Disclaimer

This repository is intended for educational and research purposes. When using or redistributing any ADS-sourced data, please comply with the ADS Terms of Use and respect licensing and attribution requirements: https://archaeologydataservice.ac.uk/about/policies/use-access-to-data/ads-terms-of-use-and-access/

⚖️ Responsible Data Sharing
This project helps make public archaeological data easier to analyze. Redistribution of ADS data should be non-commercial, for teaching/research only, and include full attribution to the original authors and ADS.

## Notes & next steps

- This is a technical demo. Next steps could include:
  - Developing of scripts for joining multiple processed datasets while avoiding filename collisions using UUIDs.
  - QA utilities to verify COCO JSON integrity and annotation quality.

