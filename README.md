# cookiecutter-taco

Cookiecutter template for TACO datasets.

## Installation

```bash
pip install cookiecutter
cookiecutter gh:tacofoundation/cookiecutter-taco
```

You'll be asked:
- `dataset_name`: Your dataset identifier
- `max_levels`: Hierarchy depth (0-4)

## Structure

```
my-dataset/
├── build.py           # DON'T EDIT - runs the build
└── dataset/           # EDIT THIS
    ├── config.py      # All configuration
    ├── taco.py        # TACO assembly
    ├── tortilla.py    # Root tortilla
    └── levels/
        ├── level0.py  # Root samples (parallel)
        └── level1.py  # Child samples (sequential)
```

**You only edit files in `dataset/`**. The `build.py` script is infrastructure.

## Configuration (dataset/config.py)

### Collection Metadata

```python
COLLECTION_ID = "my-dataset"           # Lowercase, hyphens allowed
COLLECTION_VERSION = "1.0.0"           # Semantic versioning
COLLECTION_DESCRIPTION = "..."         # What this dataset is
COLLECTION_LICENSES = ["CC-BY-4.0"]    # SPDX identifiers
COLLECTION_TITLE = "My Dataset"        # Human readable
```

### Build Settings

```python
WORKERS = 4                    # Parallel workers for level0
LEVEL0_PARALLEL = True         # Set False for debugging
LEVEL0_SAMPLE_LIMIT = None     # Limit samples for testing (None = all)
```

### Output

```python
OUTPUT_PATH = "output.tacozip"   # Output file path
OUTPUT_FORMAT = "zip"            # "zip" or "folder"
MAX_ZIP_SIZE = "4GB"             # Auto-split if exceeded
```

### Build Options

```python
CLEAN_PREVIOUS_OUTPUTS = True    # Delete old outputs before build
VALIDATE_SCHEMA = True           # Validate PIT compliance
QUIET = False                    # Show progress bars
```

### Parquet Settings

```python
# Data files
PARQUET_COMPRESSION = "zstd"
PARQUET_COMPRESSION_LEVEL = 3
PARQUET_ROW_GROUP_SIZE = 122880

# TacoCat metadata (higher compression)
TACOCAT_PARQUET_COMPRESSION_LEVEL = 13
```

## Implementation

### 1. Edit config.py

Set your metadata and build parameters.

### 2. Implement samples in levels/

Each level file needs a list of sample builder functions:

```python
# dataset/levels/level0.py (if max_levels > 0)
from tacotoolbox.datamodel import Sample
from dataset.levels import level1

def build_sample_tile_001() -> Sample:
    child_tortilla = level1.build()
    return Sample(id="tile_001", path=child_tortilla)

SAMPLES = [build_sample_tile_001]
```

```python
# dataset/levels/level1.py (leaf level, max_levels = 1)
from tacotoolbox.datamodel import Sample
from pathlib import Path

def build_sample_file_001() -> Sample:
    return Sample(id="file_001", path=Path("data/file.tif"))

SAMPLES = [build_sample_file_001]
```

### 3. Add extensions (optional)

```python
# In your sample builder
from extensions.stac import STAC

sample = Sample(id="001", path=filepath)
sample.extend_with(STAC(
    crs="EPSG:4326",
    tensor_shape=(256, 256),
    geotransform=(0, 1, 0, 0, 0, -1),
    time_start=1609459200
))
```

### 4. Test

```bash
python -m dataset.levels.level0  # Test level0 samples
python -m dataset.levels.level1  # Test level1 samples
```

### 5. Build

```bash
python build.py
```

Output: `output.tacozip` (or multiple parts if > MAX_ZIP_SIZE)

## Hierarchy Levels

- `max_levels=0`: Flat (files only)
- `max_levels=1`: level0 (folders) → level1 (files)
- `max_levels=2`: level0 → level1 → level2 (files)
- `max_levels=3`: level0 → level1 → level2 → level3 (files)
- `max_levels=4`: level0 → level1 → level2 → level3 → level4 (files)

Only level0 runs in parallel. All other levels are sequential.

## Reading Datasets

```python
import tacoreader

ds = tacoreader.load("output.tacozip")
df = ds.sql("SELECT * WHERE date > '2023-01-01'").data

# Access files via GDAL VSI
import rasterio
for path in df["internal:gdal_vsi"]:
    with rasterio.open(path) as src:
        data = src.read()
```

## Debug Mode

```python
# In config.py
LEVEL0_SAMPLE_LIMIT = 10       # Build only 10 samples
LEVEL0_PARALLEL = False        # Sequential for debugging
```

## Resources

- Spec: https://tacofoundation.github.io/specification
- TacoToolbox: https://github.com/tacofoundation/tacotoolbox
- TacoReader: https://github.com/tacofoundation/tacoreader