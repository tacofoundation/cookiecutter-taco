"""
TACO Dataset Configuration

Edit the variables below to configure your dataset.
DO NOT EDIT the COLLECTION dictionary at the bottom.
"""

from tacotoolbox.datamodel.taco import Contact, Publication, Publications

# Collection metadata
COLLECTION_ID = "{{ cookiecutter.dataset_name.lower().replace(' ', '-').replace('_', '-') }}"
COLLECTION_VERSION = "1.0.0"
COLLECTION_DESCRIPTION = "TACO dataset: {{ cookiecutter.dataset_name }}"
COLLECTION_LICENSES = ["CC-BY-4.0"]
COLLECTION_PROVIDERS = [
    Contact(name="Dataset Author", role="producer")
]
COLLECTION_TASKS = ["other"]
COLLECTION_TITLE = "{{ cookiecutter.dataset_name }}"
COLLECTION_KEYWORDS = ["taco", "dataset"]

# Optional: Dataset curators (people who maintain/curate the dataset)
# COLLECTION_CURATORS = [
#     Contact(
#         name="Your Name",
#         organization="Your Organization",
#         email="your.email@example.com",
#         role="curator",
#     ),
# ]
COLLECTION_CURATORS = None

# Optional: Publications related to the dataset
# COLLECTION_PUBLICATIONS = Publications(
#     publications=[
#         Publication(
#             doi="10.1234/example.doi",
#             citation="Author et al. (2024). Paper Title. Journal Name.",
#             summary="Brief description of paper relevance (optional)",
#         ),
#     ]
# )
COLLECTION_PUBLICATIONS = None

# Parallel processing
WORKERS = 4
LEVEL0_PARALLEL = True
LEVEL0_SAMPLE_LIMIT = None  # None = all samples, set number for debugging

# Output settings
OUTPUT_PATH = "output.tacozip"
OUTPUT_FORMAT = "auto"  # "auto", "zip", or "folder"
SPLIT_SIZE = "4GB"      # Max size per ZIP file, None = no splitting
GROUP_BY = None         # Column(s) to group by, None = no grouping
CONSOLIDATE = True      # Auto-create .tacocat/ when multiple ZIPs generated

# Build options
CLEAN_PREVIOUS_OUTPUTS = True
VALIDATE_SCHEMA = True

# Documentation
GENERATE_DOCS = True
DOWNLOAD_BASE_URL = None  # URL prefix for download links, None if not public
CATALOGUE_URL = "https://tacofoundation.github.io/catalogue"

# Parquet configuration (passed to create() as **kwargs)
PARQUET_ROW_GROUP_SIZE = 122880
PARQUET_COMPRESSION = "zstd"
PARQUET_COMPRESSION_LEVEL = 3
PARQUET_USE_DICTIONARY = True
PARQUET_WRITE_STATISTICS = True
PARQUET_DATA_PAGE_SIZE = 1048576


# INTERNAL: Auto-generated dictionaries (DO NOT EDIT)

COLLECTION = {
    "id": COLLECTION_ID,
    "dataset_version": COLLECTION_VERSION,
    "description": COLLECTION_DESCRIPTION,
    "licenses": COLLECTION_LICENSES,
    "providers": COLLECTION_PROVIDERS,
    "tasks": COLLECTION_TASKS,
    "title": COLLECTION_TITLE,
    "keywords": COLLECTION_KEYWORDS,
}

# Add optional fields if defined
if COLLECTION_CURATORS is not None:
    COLLECTION["curators"] = COLLECTION_CURATORS

if COLLECTION_PUBLICATIONS is not None:
    # Extract list from Publications pydantic model
    COLLECTION["publications"] = COLLECTION_PUBLICATIONS.publications

BUILD_CONFIG = {
    "workers": WORKERS,
    "level0_parallel": LEVEL0_PARALLEL,
    "level0_sample_limit": LEVEL0_SAMPLE_LIMIT,
    "output": OUTPUT_PATH,
    "format": OUTPUT_FORMAT,
    "split_size": SPLIT_SIZE,
    "group_by": GROUP_BY,
    "consolidate": CONSOLIDATE,
    "clean_previous_outputs": CLEAN_PREVIOUS_OUTPUTS,
    "validate_schema": VALIDATE_SCHEMA,
    "generate_docs": GENERATE_DOCS,
    "download_base_url": DOWNLOAD_BASE_URL,
    "catalogue_url": CATALOGUE_URL,
}

PARQUET_CONFIG = {
    "row_group_size": PARQUET_ROW_GROUP_SIZE,
    "compression": PARQUET_COMPRESSION,
    "compression_level": PARQUET_COMPRESSION_LEVEL,
    "use_dictionary": PARQUET_USE_DICTIONARY,
    "write_statistics": PARQUET_WRITE_STATISTICS,
    "data_page_size": PARQUET_DATA_PAGE_SIZE,
}