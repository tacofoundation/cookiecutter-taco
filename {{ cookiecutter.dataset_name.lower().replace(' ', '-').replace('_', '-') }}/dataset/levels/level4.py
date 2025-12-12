"""
Level 4 - Leaf Level

This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
    level0 (root) → level1 → level2 → level3 → level4 (LEAF - FILEs)

How to use:
    1. Define your sample builders (one function per file type)
    2. Each builder receives a context dict and returns a Sample
    3. Add extensions to extract metadata (Header, GeotiffStats, STAC, etc.)
    4. Add your builders to the SAMPLES list
    5. Run this file directly to test with mocks

Run directly to test with mocks:
    python dataset/levels/level4.py

Note:
    build(ctx) receives ONE context and creates ONE Tortilla.
    The parent level (level3) is responsible for iterating over multiple contexts.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tacotoolbox.datamodel import Sample, Tortilla
from tacotoolbox.sample.extensions.stac import STAC
from tacotoolbox.sample.extensions.scaling import Scaling
from tacotoolbox.sample.extensions.split import Split
from tacotoolbox.sample.extensions.tacotiff import Header
from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats


# Mocks
# Used when running this file directly (python dataset/levels/level4.py).
# When a parent level calls build(ctx), these are ignored.
# Each mock context simulates what the parent level would pass.

MOCKS_DIR = Path("dataset") / "mocks"

MOCK_CONTEXTS = [
    {"id": "sample01", "path": MOCKS_DIR / "sample01"},
    {"id": "sample02", "path": MOCKS_DIR / "sample02"},
]


# Tortilla parameters
# PAD_TO: pad samples to make count divisible (None = no padding)
# STRICT_SCHEMA: all samples must have identical metadata fields (recommended True)

PAD_TO = None
STRICT_SCHEMA = True


# Sample builders
# One function per file type. Each receives ONE ctx dict and returns ONE Sample.
# ctx contains whatever data the parent level passes (or MOCK_CONTEXTS when testing).
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


# Samples list
# Add all your sample builders here. Order matters for PIT schema consistency.

SAMPLES = [
    build_sample_rgb,
    build_sample_multiband,
    build_sample_singleband,
    build_sample_mask_binary,
    build_sample_mask_multiclass,
]


# Build function
# Receives ONE context dict and creates ONE Tortilla containing all samples.
# The parent level (level3) calls this function for each of its contexts.

def build(ctx: dict) -> Tortilla:
    return Tortilla(
        samples=[fn(ctx) for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )


# Validation
# Run this file directly to test your sample builders with mocks.

if __name__ == "__main__":
    print("Building level4 with mocks...")
    for ctx in MOCK_CONTEXTS:
        tortilla = build(ctx)
        print(f"{ctx['id']}: {len(tortilla.samples)} samples")
    print(tortilla.export_metadata())