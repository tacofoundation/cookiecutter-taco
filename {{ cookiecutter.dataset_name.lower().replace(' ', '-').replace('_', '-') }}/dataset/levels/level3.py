"""
Level 3{% if cookiecutter.max_levels|int == 3 %} - Leaf Level{% endif %}

{% if cookiecutter.max_levels|int == 3 %}This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
    level0 (root) → level1 → level2 → level3 (LEAF - FILEs)
{% else %}This level contains FOLDER samples. Each sample wraps a level4 Tortilla.

Structure:
    level0 (root) → level1 → level2 → level3 (FOLDERs) → level4 (FILEs)
{% endif %}
How to use:
{% if cookiecutter.max_levels|int == 3 %}    1. Define your sample builders (one function per file type)
    2. Each builder receives a context dict and returns a Sample
    3. Add extensions to extract metadata (Header, GeotiffStats, STAC, etc.)
    4. Add your builders to the SAMPLES list
{% else %}    1. Define your sample builders (one function per folder type)
    2. Each builder receives a context dict from level2
    3. Call level4.build(ctx) to create the child Tortilla
    4. Wrap it in a Sample with FIXED ID (not ctx["id"])
    5. Add your builders to the SAMPLES list
{% endif %}
Run directly to test:
    python dataset/levels/level3.py

Note:
    build(ctx) receives ONE context and creates ONE Tortilla.
    The parent level (level2) is responsible for iterating over multiple contexts.
    
    IMPORTANT: Sample IDs at level1+ must be FIXED (same for all parents).
    Only level0 can have different IDs. This ensures PIT compliance.
"""

from tacotoolbox.datamodel import Sample, Tortilla
{% if cookiecutter.max_levels|int == 3 %}# from tacotoolbox.sample.extensions.stac import STAC
# from tacotoolbox.sample.extensions.scaling import Scaling
# from tacotoolbox.sample.extensions.split import Split
# from tacotoolbox.sample.extensions.tacotiff import Header
# from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
{% else %}from dataset.levels import level4
# from tacotoolbox.sample.extensions.split import Split
# from dataset.extensions import CustomMetadata
{% endif %}
from dataset.metadata import load_contexts


# Tortilla parameters
PAD_TO = None
STRICT_SCHEMA = True


{% if cookiecutter.max_levels|int == 3 %}# Sample builders - one function per file type
def build_sample_rgb(ctx: dict) -> Sample:
    """RGB image (3 bands, uint8)"""
    sample = Sample(id="rgb", path=b"/path/to/rgb.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats())
    return sample


def build_sample_multiband(ctx: dict) -> Sample:
    """Multispectral image (10 bands, uint16)"""
    sample = Sample(id="multiband", path=b"/path/to/multiband.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats())
    return sample


def build_sample_singleband(ctx: dict) -> Sample:
    """Singleband float (DEM, indices, etc.)"""
    sample = Sample(id="singleband", path=b"/path/to/singleband.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats())
    return sample


def build_sample_mask_binary(ctx: dict) -> Sample:
    """Binary mask (0/1)"""
    sample = Sample(id="mask_binary", path=b"/path/to/mask_binary.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats(categorical=True, class_values=[0, 1]))
    return sample


def build_sample_mask_multiclass(ctx: dict) -> Sample:
    """Multiclass mask (0-5)"""
    sample = Sample(id="mask_multiclass", path=b"/path/to/mask_multiclass.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats(categorical=True, class_values=[0, 1, 2, 3, 4, 5]))
    return sample


SAMPLES = [
    build_sample_rgb,
    build_sample_multiband,
    build_sample_singleband,
    build_sample_mask_binary,
    build_sample_mask_multiclass,
]
{% else %}# Sample builders - FOLDER samples with FIXED IDs
def build_sample_train(ctx: dict) -> Sample:
    """Training split FOLDER sample wrapping level4 Tortilla."""
    child_tortilla = level4.build(ctx)
    sample = Sample(id="split_train", path=child_tortilla)
    # sample.extend_with(Split(split="train"))
    # sample.extend_with(CustomMetadata(region="north", quality_score=0.95))
    return sample


SAMPLES = [
    build_sample_train,
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
{% if cookiecutter.max_levels|int > 3 %}    import importlib
    importlib.reload(level4)
{% endif %}
    contexts = load_contexts(limit=2)
    print(f"Building level3 with {len(contexts)} contexts...")
    for ctx in contexts:
        tortilla = build(ctx)
    print(tortilla.export_metadata())