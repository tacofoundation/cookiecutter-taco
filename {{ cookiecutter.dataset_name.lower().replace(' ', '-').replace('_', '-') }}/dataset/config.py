"""
TACO Dataset Configuration

Edit the variables in the sections below to configure your dataset.
The dictionaries at the bottom are auto-generated from these variables.

DO NOT EDIT the "INTERNAL" section unless you know what you're doing.
"""

# =============================================================================
# COLLECTION METADATA
# =============================================================================

COLLECTION_ID = "{{ cookiecutter.dataset_name.lower().replace(' ', '-').replace('_', '-') }}"
COLLECTION_VERSION = "1.0.0"
COLLECTION_DESCRIPTION = "TACO dataset: {{ cookiecutter.dataset_name }}"
COLLECTION_LICENSES = ["CC-BY-4.0"]
COLLECTION_PROVIDERS = [{"name": "Dataset Author", "roles": ["producer"]}]
COLLECTION_TASKS = ["other"]
COLLECTION_TITLE = "{{ cookiecutter.dataset_name }}"
COLLECTION_KEYWORDS = ["taco", "dataset"]

# =============================================================================
# BUILD CONFIGURATION
# =============================================================================

# Parallel processing
WORKERS = 4
LEVEL0_PARALLEL = True  # Enable parallel build for level0 samples (set False for debugging)
LEVEL0_SAMPLE_LIMIT = None  # Limit number of level0 samples to build (None = all, useful for debugging)

# Output settings
OUTPUT_PATH = "output.tacozip"
OUTPUT_FORMAT = "zip"  # "zip" or "folder"
MAX_ZIP_SIZE = "4GB"

# Build options
CLEAN_PREVIOUS_OUTPUTS = True  # Auto-clean before building
VALIDATE_SCHEMA = True         # Validate PIT schema consistency
QUIET = False                  # Show progress bars and logs

# =============================================================================
# DOCUMENTATION
# =============================================================================

# Auto-generate interactive HTML and Markdown documentation after build
GENERATE_DOCS = True

# Optional: URL prefix for download links in documentation
# Leave as None if files are not publicly accessible
# Example: "https://huggingface.co/datasets/myorg/mydataset/resolve/main/"
DOWNLOAD_BASE_URL = None

# URL for "Back to Catalogue" button in HTML docs
# Set to None to hide the button
CATALOGUE_URL = "https://tacofoundation.github.io/catalogue"

# =============================================================================
# PARQUET CONFIGURATION (for data files)
# =============================================================================

PARQUET_ROW_GROUP_SIZE = 122880
PARQUET_COMPRESSION = "zstd"
PARQUET_COMPRESSION_LEVEL = 3
PARQUET_USE_DICTIONARY = True
PARQUET_WRITE_STATISTICS = True
PARQUET_DATA_PAGE_SIZE = 1048576

# =============================================================================
# TACOCAT PARQUET CONFIGURATION (for consolidated metadata)
# =============================================================================

TACOCAT_PARQUET_ROW_GROUP_SIZE = 122880
TACOCAT_PARQUET_COMPRESSION = "zstd"
TACOCAT_PARQUET_COMPRESSION_LEVEL = 13  # Higher compression for metadata-only
TACOCAT_PARQUET_USE_DICTIONARY = True
TACOCAT_PARQUET_WRITE_STATISTICS = True
TACOCAT_PARQUET_DATA_PAGE_SIZE = 1048576


# =============================================================================
# INTERNAL: Auto-generated dictionaries (DO NOT EDIT)
# =============================================================================

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

BUILD_CONFIG = {
    "workers": WORKERS,
    "level0_parallel": LEVEL0_PARALLEL,
    "level0_sample_limit": LEVEL0_SAMPLE_LIMIT,
    "output": OUTPUT_PATH,
    "format": OUTPUT_FORMAT,
    "max_zip_size": MAX_ZIP_SIZE,
    "clean_previous_outputs": CLEAN_PREVIOUS_OUTPUTS,
    "validate_schema": VALIDATE_SCHEMA,
    "quiet": QUIET,
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

TACOCAT_PARQUET_CONFIG = {
    "row_group_size": TACOCAT_PARQUET_ROW_GROUP_SIZE,
    "compression": TACOCAT_PARQUET_COMPRESSION,
    "compression_level": TACOCAT_PARQUET_COMPRESSION_LEVEL,
    "use_dictionary": TACOCAT_PARQUET_USE_DICTIONARY,
    "write_statistics": TACOCAT_PARQUET_WRITE_STATISTICS,
    "data_page_size": TACOCAT_PARQUET_DATA_PAGE_SIZE,
}