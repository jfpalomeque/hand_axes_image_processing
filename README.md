# Hand-axes Image Processing & COCO Generator pipeline

This repository contains utilities and scripts to prepare and process image collections of archaeological artifacts for computer vision workflows. Specifically, it was initially developed to work with the Lower Palaeolithic hand-axes / bifaces dataset from the Archaeology Data Service (ADS), when bulk downloading the images and data as explained in this other [repository](repo link).

 The primary goals are:

- Generate a COCO-format JSON (blank or partially populated) for the collection.
- Convert image filenames to UUID-based names while producing a mapping file.
- Run an image segmentation pipeline over a collection and embed annotations into the COCO JSON.

The code is lightweight and intended for researchers who want to convert archaeological image collections into formats suitable for machine learning / computer vision experiments.

## 📚 Citation

If you use the underlying ADS bifaces data included or referenced here, please cite the original source:

**Lower Palaeolithic technology, raw material and population ecology (bifaces)**
*Gilbert Marshall, David Dupplaw, Derek Roe, Clive Gamble (2002)*
DOI: [10.5284/1000354](https://doi.org/10.5284/1000354)

## How to use it

Create a Python virtual environment and install dependencies. Two common options:

PowerShell (Windows):

```powershell
# (preferred) create and activate venv
python -m venv .venv; .\.venv\Scripts\Activate.ps1
# if you have a requirements.txt
pip install -r requirements.txt
# OR if you manage dependencies with pyproject/poetry
pip install poetry; poetry install
```

Then run the main processing script:

```powershell
python main.py
```

What `main.py` does (default behaviour):

- Reads collection metadata from `dataset_info.md`.
- Generates a blank COCO JSON (uses collection metadata for description, contributor, year, etc.) and saves it as `<collection_short_name>.json` (or `coco.json`).
- Converts images found in `original_images_test/` into UUID-named copies in `uuid_images_test/` and writes a UUID mapping CSV.
- Ensures at least one default category exists in the COCO JSON (id=1, name="object").
- Runs the segmentation pipeline in `src/segment_collection_images.py` to populate image/annotation entries.

Adjust the paths inside `main.py` (or copy/extend it) to work with your own `original_images/` folder and desired output locations.

## Repository contents

- `main.py` — top-level runner that generates COCO JSON, creates UUID-mapped images, and runs segmentation.
- `pyproject.toml` — project metadata / dependency configuration (if used).
- `dataset_info.md` — short metadata used to populate the COCO JSON header.
- `DB_overview.md` — copied dataset overview for the original bifaces dataset.
- `bifaces_Marshall_et_al_2002.json` — exported metadata (local copy / snapshot).
- `biface_records_online.csv` — CSV with artifact records (if generated).
- `original_images/` and `original_images_test/` — source image folders (example/test images included).
- `uuid_images_test/` — example output folder created by the UUID generator.
- `src/` — library modules used by the pipeline, including:
	- `COCO_JSON_gen.py` — COCO JSON creation utilities
	- `UUID_generator.py` — creates UUID filenames and mapping
	- `segment_collection_images.py` — segmentation pipeline wiring
	- `segment_unique_object.py` — routines for single-image segmentation
	- `coll_info.py` — collection metadata extraction

## Example workflow

1. Place your images in `original_images/` (or `original_images_test/` for quick tests).
2. Edit `dataset_info.md` with collection metadata (title, year, contributor, etc.).
3. Run `python main.py` — this will write a COCO JSON and populate `uuid_images_test/`.

## Why this repo?

The Archaeology Data Service (ADS) provides vital curated datasets, but many analysis workflows require data in ML-friendly formats (COCO JSON, consistent filenames). This project bridges that gap by:

- allowing offline, large-scale processing of archaeological image collections,
- producing standard COCO outputs suitable for training/annotation tools,
- keeping a clear mapping between original filenames and anonymized UUID filenames.

## ⚠️ Disclaimer

This repository is intended for educational and research purposes. When using or redistributing any ADS-sourced data, please comply with the ADS Terms of Use and respect licensing and attribution requirements: https://archaeologydataservice.ac.uk/about/policies/use-access-to-data/ads-terms-of-use-and-access/

⚖️ Responsible Data Sharing
This project helps make public archaeological data easier to analyze. Redistribution of ADS data should be non-commercial, for teaching/research only, and include full attribution to the original authors and ADS.

## Notes & next steps

- If you want automated installation, add a `requirements.txt` or a Poetry lock file (if not present).
- Consider adding a small example notebook or script that loads the generated COCO JSON and visualises images + annotations.

If you'd like, I can add a short usage example script or generate a minimal `requirements.txt` from `pyproject.toml`.

---
Generated README for the repository.
