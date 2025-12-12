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
├── create.py          # DON'T EDIT - runs the build
└── dataset/           # EDIT THIS
    ├── config.py      # All configuration
    ├── taco.py        # TACO assembly
    ├── tortilla.py    # Root tortilla
    └── levels/
        ├── level0.py  # Root samples (parallel)
        └── level1.py  # Child samples (sequential)
```

**You only edit files in `dataset/`**. The `create.py` script is infrastructure.

## Configuration (dataset/config.py)

### Collection Metadata

```python
from tacotoolbox.taco.datamodel import Contact

COLLECTION_ID = "my-dataset"           # Lowercase, hyphens allowed
COLLECTION_VERSION = "1.0.0"           # Semantic versioning
COLLECTION_DESCRIPTION = "..."         # What this dataset is
COLLECTION_LICENSES = ["CC-BY-4.0"]    # SPDX identifiers
COLLECTION_PROVIDERS = [               # Contact objects
    Contact(name="Author Name", role="producer")
]
COLLECTION_TITLE = "My Dataset"        # Human readable
COLLECTION_TASKS = ["classification"]  # ML task types
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
OUTPUT_FORMAT = "auto"           # "auto", "zip", or "folder"
SPLIT_SIZE = "4GB"               # Auto-split if exceeded (None = no split)
GROUP_BY = None                  # Column(s) to group by (None = no grouping)
CONSOLIDATE = True               # Auto-create .tacocat/ when multiple ZIPs
```

When `CONSOLIDATE=True` and multiple ZIPs are created (via splitting or grouping), a `.tacocat/` folder is automatically generated with consolidated metadata for efficient querying.

### Documentation

```python
GENERATE_DOCS = True             # Auto-generate HTML and Markdown docs
DOWNLOAD_BASE_URL = None         # Optional: URL prefix for download links
CATALOGUE_URL = "..."            # URL for "Back to Catalogue" button
```

The build script automatically generates:
- `index.html` - Interactive documentation with PIT visualization and maps
- `README.md` - GitHub-ready markdown documentation
- `COLLECTION.json` - Dataset metadata (standalone or in `.tacocat/`)

Set `DOWNLOAD_BASE_URL` to add download buttons in the HTML docs:
```python
DOWNLOAD_BASE_URL = "https://huggingface.co/datasets/myorg/mydataset/resolve/main/"
```

### Build Options

```python
CLEAN_PREVIOUS_OUTPUTS = True    # Delete old outputs before build
VALIDATE_SCHEMA = True           # Validate PIT compliance
```

To control logging verbosity, use `tacotoolbox.verbose()` in your code:
```python
import tacotoolbox
tacotoolbox.verbose(True)   # Show logs
tacotoolbox.verbose(False)  # Hide logs
```

### Parquet Settings

```python
PARQUET_COMPRESSION = "zstd"
PARQUET_COMPRESSION_LEVEL = 3
PARQUET_ROW_GROUP_SIZE = 122880
```

## Implementation

### 1. Edit config.py

Set your metadata and build parameters.

### 2. Implement samples in levels/

Each level file needs a list of sample builder functions.

**IMPORTANT: PIT Compliance**
- **level0 (root)**: Can have different IDs per sample
- **level1+**: Must use FIXED IDs (same for all parents) to ensure PIT compliance

```python
# dataset/levels/level0.py (root - IDs can be different)
from tacotoolbox.datamodel import Sample
from dataset.levels import level1

def build_sample_tile_001() -> Sample:
    child_tortilla = level1.build({"id": "tile_001", "path": ...})
    return Sample(id="tile_001", path=child_tortilla)  # ✓ ctx["id"] OK

def build_sample_tile_002() -> Sample:
    child_tortilla = level1.build({"id": "tile_002", "path": ...})
    return Sample(id="tile_002", path=child_tortilla)  # ✓ Different ID OK

SAMPLES = [build_sample_tile_001, build_sample_tile_002]
```

```python
# dataset/levels/level1.py (level1+ - IDs must be FIXED)
from tacotoolbox.datamodel import Sample
from dataset.levels import level2

def build_sample_date(ctx: dict) -> Sample:
    child_tortilla = level2.build(ctx)
    return Sample(id="date_2023_05", path=child_tortilla)  # ✓ FIXED ID

SAMPLES = [build_sample_date]
```

```python
# dataset/levels/level2.py (leaf level example)
from tacotoolbox.datamodel import Sample
from pathlib import Path

def build_sample_rgb(ctx: dict) -> Sample:
    return Sample(id="rgb", path=ctx["path"] / "rgb.tif")  # ✓ FIXED ID

def build_sample_nir(ctx: dict) -> Sample:
    return Sample(id="nir", path=ctx["path"] / "nir.tif")  # ✓ FIXED ID

SAMPLES = [build_sample_rgb, build_sample_nir]
```

This ensures all root samples have identical internal structure:
```
tile_001 → [date_2023_05] → [rgb, nir]
tile_002 → [date_2023_05] → [rgb, nir]  # Same structure!
```

### 3. Add extensions (optional)

```python
# In your sample builder
from tacotoolbox.sample.extensions.stac import STAC

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
python dataset/levels/level0.py  # Test level0 samples
python dataset/levels/level1.py  # Test level1 samples
python dataset/taco.py           # Test complete TACO
```

### 5. Build

```bash
python create.py
```

Output:
- `output.tacozip` (or multiple parts if > SPLIT_SIZE)
- `.tacocat/` folder (if multi-part and CONSOLIDATE=True)
- `COLLECTION.json` (standalone if single file)
- `index.html` (interactive docs)
- `README.md` (markdown docs)

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

# Single ZIP
ds = tacoreader.load("output.tacozip")

# Multiple ZIPs (consolidated)
ds = tacoreader.load(".tacocat")

# Query and filter
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
GENERATE_DOCS = False          # Skip docs generation
SPLIT_SIZE = None              # No splitting
CONSOLIDATE = False            # No consolidation
```

```python
# In your code
import tacotoolbox
tacotoolbox.verbose("debug")   # Very detailed logging
```

## Advanced: Grouping by Metadata

Split dataset by metadata column instead of size:

```python
# In config.py
SPLIT_SIZE = None              # Disable size-based splitting
GROUP_BY = "spatialgroup:code" # Create one ZIP per spatial group
CONSOLIDATE = True             # Auto-consolidate into .tacocat/
```

Output:
```
output_sg0000.tacozip
output_sg0001.tacozip
output_sg0002.tacozip
.tacocat/               # Consolidated metadata for all groups
```

## Resources

- Spec: https://tacofoundation.github.io/specification
- TacoToolbox: https://github.com/tacofoundation/tacotoolbox
- TacoReader: https://github.com/tacofoundation/tacoreader