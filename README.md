# Hand-axes Image Processing & COCO Generator

This repository contains a Python workflow for preparing archaeological image collections for computer-vision analysis. It was developed using the Archaeology Data Service (ADS) collection *Lower Palaeolithic technology, raw material and population ecology (bifaces)* by Gilbert Marshall, David Dupplaw, Derek Roe and Clive Gamble (2002), DOI: https://doi.org/10.5284/1000354.

The workflow has three main functions:

- create UUID-named copies of source images while retaining a mapping to the original filenames;
- write the UUID into the copied image metadata;
- generate a COCO-style JSON structure containing image records, segmentation masks and bounding boxes.

The ADS collection remains the authoritative source. Original ADS images are not redistributed in this repository.

## Scope of the case study

The complete downloaded image collection contained 10,668 images representing 3,556 bifaces. The UUID-renaming stage was run across all 10,668 images.

The segmentation output preserved in this repository, `bifaces_Marshall_et_al_2002.json`, is a proof of concept containing 100 image entries and 100 automatically generated annotations. These annotations have not been manually validated as ground truth and should not be interpreted as an accuracy benchmark.

## Requirements

Python 3.12 or later is recommended.

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Input structure

Place source images in:

```text
original_images/
```

Supported image extensions include JPEG, PNG, TIFF, BMP and GIF.

Collection-level metadata are read from `dataset_info.md`.

## Running the pipeline

Run:

```bash
python main.py
```

The default workflow:

1. reads collection metadata from `dataset_info.md`;
2. creates a COCO-style JSON file;
3. assigns a version 4 UUID to each source image;
4. copies each image to `uuid_images/` using the UUID as the filename;
5. writes the UUID to the copied image's EXIF `UserComment` field;
6. records the original-to-UUID filename mapping in `uuid_images/uuid_mapping.csv`;
7. segments the main object in each copied image and appends the resulting mask and bounding box to the JSON file.

## Segmentation assumptions

The segmentation procedure was designed for the photographic characteristics of the ADS biface collection: one artefact per image, usually positioned against a dark background.

The processing sequence converts the image to greyscale, applies Gaussian smoothing, calculates an Otsu threshold, performs morphological cleaning, selects the largest external contour, and creates a filled binary mask plus an axis-aligned bounding box.

This is deliberately a lightweight classical computer-vision approach. Results depend on the photographic setup and may fail where object/background contrast is poor, several objects are present, shadows are strong, or an artefact touches the image boundary.

The annotation JSON uses UUID strings as image and annotation identifiers. Software that requires strictly integer COCO identifiers may need a conversion step.

## Outputs

The workflow produces:

- a JSON file named from `Collection_short_name` in `dataset_info.md`;
- UUID-named image copies in `uuid_images/`;
- `uuid_images/uuid_mapping.csv`, linking original filenames to UUID filenames.

The repository includes the 100-image proof-of-concept annotation JSON used to document the segmentation stage. The original ADS images are excluded.

## Data provenance and reuse

The source archaeological material is:

> Marshall, G., Dupplaw, D., Roe, D. and Gamble, C. (2002). *Lower Palaeolithic technology, raw material and population ecology (bifaces).* Archaeology Data Service. https://doi.org/10.5284/1000354

Users must consult the ADS Terms of Use and the conditions attached to the original collection before downloading, reusing or redistributing ADS material:

https://archaeologydataservice.ac.uk/about/policies/use-access-to-data/ads-terms-of-use-and-access/

The MIT licence in this repository applies only to the software authored for this project. It does not change the licence or reuse conditions of the source ADS data or images.

## Citation

Citation metadata for this software are provided in `CITATION.cff`. A permanent DOI will be added after the software release is archived with Zenodo.

## Related repository

The companion scraper used to retrieve the ADS records and images is available at:

https://github.com/jfpalomeque/hand_axes_database_downloader

## Licence

Software in this repository is released under the MIT License. See `LICENSE`.
