"""
Level 1{% if cookiecutter.max_levels|int == 1 %} - Leaf Level{% endif %}

{% if cookiecutter.max_levels|int == 1 %}This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
    level0 (root) -> level1 (LEAF - FILEs)
{% else %}This level contains FOLDER samples. Each sample wraps a level2 Tortilla.

Structure:
    level0 (root) -> level1 (FOLDERs) -> level2 -> ... -> level{{ cookiecutter.max_levels }} (FILEs)
{% endif %}
How to use:
{% if cookiecutter.max_levels|int == 1 %}    1. Define your sample builders (one function per file type)
    2. Each builder receives a context dict and returns a Sample
    3. Add extensions to extract metadata (Header, GeotiffStats, STAC, etc.)
    4. Add your builders to the SAMPLES list
{% else %}    1. Define your sample builders (one function per folder type)
    2. Each builder receives a context dict from level0
    3. Call level2.build(ctx) to create the child Tortilla
    4. Wrap it in a Sample with FIXED ID (not ctx["id"])
    5. Add your builders to the SAMPLES list
{% endif %}
Run directly to test:
    python dataset/levels/level1.py

Note:
    build(ctx) receives ONE context and creates ONE Tortilla.
    The parent level (level0) is responsible for iterating over multiple contexts.

    IMPORTANT: Sample IDs at level1+ must be FIXED (same for all parents).
    Only level0 can have different IDs. This ensures PIT compliance.
"""

from tacotoolbox.datamodel import Sample, Tortilla
{% if cookiecutter.max_levels|int == 1 %}# from tacotoolbox.sample.extensions.tacotiff import Header
# from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
# from tacotoolbox.sample.extensions.stac import STAC
# from tacotoolbox.sample.extensions.istac import ISTAC
# from tacotoolbox.sample.extensions.scaling import Scaling
# from tacotoolbox.sample.extensions.split import Split
# from dataset.extensions import CustomMetadata
{% else %}from dataset.levels import level2
# from dataset.extensions import CustomMetadata
{% endif %}
from dataset.metadata import load_contexts


# Tortilla parameters
PAD_TO = None
STRICT_SCHEMA = True


{% if cookiecutter.max_levels|int == 1 %}# Sample builders - one function per file type
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


SAMPLES = [
    build_sample_input,
    build_sample_target,
]
{% else %}# Sample builders - FOLDER samples with FIXED IDs
def build_sample_images(ctx: dict) -> Sample:
    """Images FOLDER sample wrapping level2 Tortilla."""
    child_tortilla = level2.build(ctx)
    sample = Sample(id="images", path=child_tortilla)
    # sample.extend_with(CustomMetadata(region="north", quality_score=0.95))
    return sample


SAMPLES = [
    build_sample_images,
]
{% endif %}

# Build function - receives ONE context, creates ONE Tortilla
def build(ctx: dict) -> Tortilla:
    return Tortilla(
        samples=[fn(ctx) for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )


# Validation - run directly to test
if __name__ == "__main__":
{% if cookiecutter.max_levels|int > 1 %}    import importlib
    importlib.reload(level2)
{% endif %}
    contexts = load_contexts(limit=2)
    print(f"Building level1 with {len(contexts)} contexts...")
    for ctx in contexts:
        tortilla = build(ctx)
    print(tortilla.export_metadata())