# cookiecutter-taco

Cookiecutter template for TACO datasets.

## Requirements

- Python >= 3.10
- tacotoolbox >= 0.22.0
- tacoreader >= 2.0.0
- jinja2 >= 3.0
- cookiecutter >= 2.0
- markdown >= 3.0

## Installation

```bash
pip install cookiecutter
cookiecutter gh:tacofoundation/cookiecutter-taco
```

You'll be asked:
- `dataset_name`: Your dataset identifier
- `max_levels`: Hierarchy depth (0-4)

Then install dependencies:
```bash
cd my-dataset
pip install -r requirements.txt
```

## Structure

```
my-dataset/
├── requirements.txt
└── dataset/
    ├── config.py       # All configuration
    ├── metadata.py     # Load contexts
    ├── extensions.py   # Custom extensions
    ├── create.py       # Build orchestration
    ├── taco.py         # TACO assembly
    ├── tortilla.py     # Root tortilla
    └── levels/
        ├── level0.py   # Root samples (parallel)
        ├── level1.py   # Child samples (sequential)
        └── ...
```

**All files are in `dataset/`**. Edit them to customize your dataset.

## Configuration (dataset/config.py)

### Collection Metadata

```python
from tacotoolbox.datamodel.taco import Provider, Curator

COLLECTION_ID = "my-dataset"           # Lowercase, hyphens allowed
COLLECTION_VERSION = "1.0.0"           # Semantic versioning
COLLECTION_DESCRIPTION = "..."         # What this dataset is
COLLECTION_LICENSES = ["CC-BY-4.0"]    # SPDX identifiers
COLLECTION_PROVIDERS = [               # Provider objects
    Provider(name="Author Name", roles=["producer"])
]
COLLECTION_TITLE = "My Dataset"        # Human readable
COLLECTION_TASKS = ["classification"]  # ML task types

# Optional: Dataset curators
COLLECTION_CURATORS = [
    Curator(
        name="Your Name",
        organization="Your Organization", 
        email="your.email@example.com",
    ),
]
```

### DataFrame Backend

```python
DATAFRAME_BACKEND = "pandas"  # "pyarrow", "polars", "pandas"
```

Controls how metadata is displayed when testing levels. Uses `tacoreader.use()` internally.

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
THEME_COLOR = "#4CAF50"          # Primary color for HTML docs
DATASET_EXAMPLE_PATH = None      # Path for code examples (None = auto)
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

### 1. Edit dataset/config.py

Set your metadata and build parameters.

### 2. Edit dataset/metadata.py

Implement `load_contexts()` to load your dataset metadata:

```python
def load_contexts(limit: float | int | None = None) -> list[dict]:
    """Load dataset metadata and return list of context dicts."""
    # Load from CSV, Parquet, filesystem, database, etc.
    contexts = [
        {"id": "sample01", "path": b"/path/to/sample01"},
        {"id": "sample02", "path": b"/path/to/sample02"},
    ]
    
    # Apply limit if specified
    if limit is not None:
        if isinstance(limit, float):
            count = int(len(contexts) * limit) or 1
            return contexts[:count]
        else:
            return contexts[:limit]
    
    return contexts
```

### 3. Implement samples in dataset/levels/

Each level file needs a list of sample builder functions.

**IMPORTANT: PIT Compliance**
- **level0 (root)**: Can have different IDs per sample (uses `ctx["id"]`)
- **level1+**: Must use FIXED IDs (same for all parents) to ensure PIT compliance

```python
# dataset/levels/level0.py (root - IDs can be different)
from tacotoolbox.datamodel import Sample
from dataset.levels import level1

def build_sample_tile(ctx: dict) -> Sample:
    """Build one root sample using ctx["id"]."""
    child_tortilla = level1.build(ctx)
    return Sample(id=ctx["id"], path=child_tortilla)  # ✓ ctx["id"] OK

SAMPLES = [build_sample_tile]
```

```python
# dataset/levels/level1.py (level1+ - IDs must be FIXED)
from tacotoolbox.datamodel import Sample
from dataset.levels import level2

def build_sample_date(ctx: dict) -> Sample:
    """Build date folder - ID is FIXED."""
    child_tortilla = level2.build(ctx)
    return Sample(id="date_2023_05", path=child_tortilla)  # ✓ FIXED ID

SAMPLES = [build_sample_date]
```

```python
# dataset/levels/level2.py (leaf level example)
from tacotoolbox.datamodel import Sample

def build_sample_rgb(ctx: dict) -> Sample:
    """RGB image - ID is FIXED."""
    return Sample(id="rgb", path=b"/path/to/rgb.tif")  # ✓ FIXED ID

def build_sample_nir(ctx: dict) -> Sample:
    """NIR image - ID is FIXED."""
    return Sample(id="nir", path=b"/path/to/nir.tif")  # ✓ FIXED ID

SAMPLES = [build_sample_rgb, build_sample_nir]
```

This ensures all root samples have identical internal structure:
```
tile_001 → [date_2023_05] → [rgb, nir]
tile_002 → [date_2023_05] → [rgb, nir]  # Same structure!
```

### 4. Add extensions (optional)

```python
# In your sample builder
from tacotoolbox.sample.extensions.stac import STAC

sample = Sample(id="001", path=b"/path/to/file.tif")
sample.extend_with(STAC(
    crs="EPSG:4326",
    tensor_shape=(256, 256),
    geotransform=(0, 1, 0, 0, 0, -1),
    time_start=1609459200
))
```

Or create custom extensions in `dataset/extensions.py`:

```python
import pyarrow as pa
from tacotoolbox.sample.datamodel import SampleExtension

class CustomMetadata(SampleExtension):
    region: str
    quality_score: float
    
    def get_schema(self) -> dict[str, pa.DataType]:
        return {
            "custom:region": pa.string(),
            "custom:quality_score": pa.float32(),
        }
    
    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "custom:region": "Geographic region",
            "custom:quality_score": "Quality assessment score (0-1)",
        }
    
    def _compute(self, sample) -> pa.Table:
        schema = pa.schema([
            (name, dtype) for name, dtype in self.get_schema().items()
        ])
        data = {
            "custom:region": [self.region],
            "custom:quality_score": [self.quality_score],
        }
        return pa.table(data, schema=schema)
```

Then use it in your builders:
```python
from dataset.extensions import CustomMetadata

sample.extend_with(CustomMetadata(region="north", quality_score=0.95))
```

### 5. Test

Run levels as modules to test them individually:

```bash
# Test individual levels
python -m dataset.levels.level0
python -m dataset.levels.level1
python -m dataset.levels.level2

# Test complete tortilla
python -m dataset.tortilla

# Test complete TACO
python -m dataset.taco
```

### 6. Build

```bash
python -m dataset.create
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

# Set DataFrame backend (optional)
tacoreader.use("pandas")  # "pyarrow", "polars", "pandas"

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
# In dataset/config.py
LEVEL0_SAMPLE_LIMIT = 10       # Build only 10 samples
LEVEL0_PARALLEL = False        # Sequential for debugging
GENERATE_DOCS = False          # Skip docs generation
SPLIT_SIZE = None              # No splitting
CONSOLIDATE = False            # No consolidation
DATAFRAME_BACKEND = "polars"   # Readable output when testing
```

```python
# In your code
import tacotoolbox
tacotoolbox.verbose("debug")   # Very detailed logging
```

Test with limited samples:
```bash
# This will use LEVEL0_SAMPLE_LIMIT from config
python -m dataset.taco
```

## Advanced: Grouping by Metadata

Split dataset by metadata column instead of size:

```python
# In dataset/config.py
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