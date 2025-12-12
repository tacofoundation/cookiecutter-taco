"""
Level 0 - Root Level

{% if cookiecutter.max_levels|int == 0 %}This is the ROOT and LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
    level0 (root - FILEs)
{% else %}This is the ROOT level of your TACO hierarchy. Each sample here becomes a
top-level entry in your dataset.

Structure:
    level0 (root FOLDERs) → level1 → ... → level{{ cookiecutter.max_levels }} (FILEs)
{% endif %}
How to use:
{% if cookiecutter.max_levels|int == 0 %}    1. Define your sample builders (one function per file type)
    2. Each builder receives a context dict and returns a Sample
    3. Add extensions to extract metadata (Header, GeotiffStats, STAC, etc.)
    4. Add your builders to the SAMPLES list
    5. Run this file directly to test with mocks
{% else %}    1. Define your sample builders (one function per root folder type)
    2. Each builder receives a context dict (from MOCK_CONTEXTS or real data)
    3. Call level1.build(ctx) to create the child Tortilla
    4. Wrap it in a Sample with type=FOLDER
    5. Add your builders to the SAMPLES list
{% endif %}
Run directly to test with mocks:
    python dataset/levels/level0.py

Note:
    level0.build() iterates over ALL contexts and creates the root Tortilla.
    This is the only level that iterates - all others receive a single context.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pyarrow as pa
from tacotoolbox.datamodel import Sample, Tortilla
from tacotoolbox.sample.datamodel import SampleExtension
{% if cookiecutter.max_levels|int == 0 %}from tacotoolbox.sample.extensions.stac import STAC
from tacotoolbox.sample.extensions.scaling import Scaling
from tacotoolbox.sample.extensions.split import Split
from tacotoolbox.sample.extensions.tacotiff import Header
from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
{% else %}from dataset.levels import level1
{% endif %}

# Mocks
# Used when running this file directly.
# In production, replace with real data loading.

MOCKS_DIR = Path("dataset") / "mocks"

MOCK_CONTEXTS = [
    {"id": "sample01", "path": MOCKS_DIR / "sample01"},
    {"id": "sample02", "path": MOCKS_DIR / "sample02"},
]


# Tortilla parameters

PAD_TO = None
STRICT_SCHEMA = True


{% if cookiecutter.max_levels|int == 0 %}# Sample builders
# One function per file type. Each receives ONE ctx dict and returns ONE Sample.
# 
# Available extensions:
#   Header()        - TACOTIFF binary header for fast reading
#   GeotiffStats()  - Per-band statistics (min, max, mean, std, percentiles)
#   GeotiffStats(categorical=True, class_values=[0,1,2]) - Class probabilities
#   STAC(crs=..., tensor_shape=..., geotransform=..., time_start=...) - Spatiotemporal
#   Scaling(scale_factor=..., scale_offset=...) - Data unpacking transformation
#   Split(split="train"|"test"|"validation") - Dataset partition

def build_sample_rgb(ctx: dict) -> Sample:
    """RGB image (3 bands, uint8)"""
    sample = Sample(id="rgb", path=ctx["path"] / "rgb_uint8.tif")
    sample.extend_with(Header())
    sample.extend_with(GeotiffStats())
    return sample


def build_sample_multiband(ctx: dict) -> Sample:
    """Multispectral image (10 bands, uint16)"""
    sample = Sample(id="multiband", path=ctx["path"] / "multiband_uint16.tif")
    sample.extend_with(Header())
    sample.extend_with(GeotiffStats())
    return sample


def build_sample_singleband(ctx: dict) -> Sample:
    """Singleband float (DEM, indices, etc.)"""
    sample = Sample(id="singleband", path=ctx["path"] / "singleband_float32.tif")
    sample.extend_with(Header())
    sample.extend_with(GeotiffStats())
    return sample


def build_sample_mask_binary(ctx: dict) -> Sample:
    """Binary mask (0/1)"""
    sample = Sample(id="mask_binary", path=ctx["path"] / "mask_binary.tif")
    sample.extend_with(Header())
    sample.extend_with(GeotiffStats(categorical=True, class_values=[0, 1]))
    return sample


def build_sample_mask_multiclass(ctx: dict) -> Sample:
    """Multiclass mask (0-5)"""
    sample = Sample(id="mask_multiclass", path=ctx["path"] / "mask_multiclass.tif")
    sample.extend_with(Header())
    sample.extend_with(GeotiffStats(categorical=True, class_values=[0, 1, 2, 3, 4, 5]))
    return sample


SAMPLES = [
    build_sample_rgb,
    build_sample_multiband,
    build_sample_singleband,
    build_sample_mask_binary,
    build_sample_mask_multiclass,
]
{% else %}# Custom extension example
# Location metadata for spatial datasets.

class TileMetadata(SampleExtension):
    """Extension that adds tile/location metadata."""
    
    tile_id: str
    region: str
    utm_zone: int
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([
            pa.field("tile:id", pa.string()),
            pa.field("tile:region", pa.string()),
            pa.field("tile:utm_zone", pa.int32()),
        ])
    
    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "tile:id": "Tile identifier (e.g., MGRS grid)",
            "tile:region": "Geographic region name",
            "tile:utm_zone": "UTM zone number",
        }
    
    def _compute(self, sample: Sample) -> pa.Table:
        return pa.Table.from_pydict({
            "tile:id": [self.tile_id],
            "tile:region": [self.region],
            "tile:utm_zone": [self.utm_zone],
        }, schema=self.get_schema())


# Sample builders
# One function per folder type. Each receives ONE ctx dict and returns ONE Sample (FOLDER).

def build_sample_tile(ctx: dict) -> Sample:
    """Tile FOLDER sample wrapping level1 Tortilla."""
    child_tortilla = level1.build(ctx)
    sample = Sample(id=ctx["id"], path=child_tortilla)
    sample.extend_with(TileMetadata(
        tile_id=f"T30SYJ_{ctx['id']}",
        region="Valencia",
        utm_zone=30,
    ))
    return sample


SAMPLES = [
    build_sample_tile,
]
{% endif %}

# Build function
# This is the ROOT level - it iterates over ALL contexts and creates the final Tortilla.

def build(contexts: list[dict] | None = None) -> Tortilla:
    contexts = contexts if contexts is not None else MOCK_CONTEXTS
{% if cookiecutter.max_levels|int == 0 %}    return Tortilla(
        samples=[fn(ctx) for ctx in contexts for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )
{% else %}    return Tortilla(
        samples=[fn(ctx) for ctx in contexts for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )
{% endif %}

# Validation

if __name__ == "__main__":
{% if cookiecutter.max_levels|int > 0 %}    import importlib
    importlib.reload(level1)
{% endif %}
    print("Building level0 with mocks...")
    tortilla = build()
    print(f"Created {len(tortilla.samples)} root samples")
    print(tortilla.export_metadata())