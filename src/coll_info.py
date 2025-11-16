"""
This module extracts collection information from the first block on file README.md.
The block is expected to be delimited by '---' and '---' lines.
The extracted information will be saved in a dictionary for further use in the pipeline.
"""
import yaml

def extract_collection_info(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if content.startswith('---'):
        _, header, body = content.split('---', 2)
        meta = yaml.safe_load(header)
        body = body.strip()
    else:
        meta, body = {}, content

    return meta

