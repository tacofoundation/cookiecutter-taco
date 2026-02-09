"""
Level 4 - Leaf Level

This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
    level0 (root) -> level1 -> level2 -> level3 -> level4 (LEAF - FILEs)

How to use:
    1. Define your sample builders (one function per file type)
    2. Each builder receives a context dict and returns a Sample
    3. Add extensions to extract metadata (Header, GeotiffStats, STAC, etc.)
    4. Add your builders to the SAMPLES list

Run directly to test:
    python dataset/levels/level4.py

Note:
    build(ctx) receives ONE context and creates ONE Tortilla.
    The parent level (level3) is responsible for iterating over multiple contexts.

    IMPORTANT: Sample IDs at level1+ must be FIXED (same for all parents).
    Only level0 can have different IDs. This ensures PIT compliance.
"""

from tacotoolbox.datamodel import Sample, Tortilla
# from tacotoolbox.sample.extensions.tacotiff import Header
# from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
# from tacotoolbox.sample.extensions.stac import STAC
# from tacotoolbox.sample.extensions.istac import ISTAC
# from tacotoolbox.sample.extensions.scaling import Scaling
# from tacotoolbox.sample.extensions.split import Split
# from dataset.extensions import CustomMetadata

from dataset.metadata import load_contexts


# Tortilla parameters
PAD_TO = None
STRICT_SCHEMA = True


# Sample builders - one function per file type
def build_sample_input(ctx: dict) -> Sample:
    """Input data (e.g., satellite image, sensor data)."""
    # MOCK: replace b"..." with real path, e.g.: path=ctx["image_path"].encode()
    sample = Sample(id="input", path=b"mock input data")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats())
    # sample.extend_with(STAC(datetime="2024-01-15", geometry="POINT(0 0)"))
    return sample


def build_sample_target(ctx: dict) -> Sample:
    """Target data (e.g., label mask, ground truth)."""
    # MOCK: replace b"..." with real path, e.g.: path=ctx["mask_path"].encode()
    sample = Sample(id="target", path=b"mock target data")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats(categorical=True, class_values=[0, 1]))
    return sample


# Samples list - order matters for PIT schema consistency
SAMPLES = [
    build_sample_input,
    build_sample_target,
]


# Build function - receives ONE context, creates ONE Tortilla
def build(ctx: dict) -> Tortilla:
    return Tortilla(
        samples=[fn(ctx) for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )


# Validation - run directly to test
if __name__ == "__main__":
    contexts = load_contexts(limit=2)
    print(f"Building level4 with {len(contexts)} contexts...")
    for ctx in contexts:
        tortilla = build(ctx)
    print(tortilla.export_metadata())