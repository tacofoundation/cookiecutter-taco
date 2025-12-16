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
{% else %}    1. Define your sample builders (one function per root folder type)
    2. Each builder receives a context dict from load_contexts()
    3. Call level1.build(ctx) to create the child Tortilla
    4. Wrap it in a Sample with ctx["id"] as ID
    5. Add your builders to the SAMPLES list
{% endif %}
Run directly to test:
    python dataset/levels/level0.py

Note:
    level0.build() iterates over ALL contexts and creates the root Tortilla.
    This is the only level that iterates - all others receive a single context.
    Parallel processing is controlled by config.py (LEVEL0_PARALLEL, WORKERS).
"""

from tacotoolbox.datamodel import Sample, Tortilla
{% if cookiecutter.max_levels|int == 0 %}# from tacotoolbox.sample.extensions.stac import STAC
# from tacotoolbox.sample.extensions.scaling import Scaling
# from tacotoolbox.sample.extensions.split import Split
# from tacotoolbox.sample.extensions.tacotiff import Header
# from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
# from dataset.extensions import CustomMetadata
{% else %}from dataset.levels import level1
# from dataset.extensions import CustomMetadata
{% endif %}
from dataset.metadata import load_contexts
from dataset.config import LEVEL0_SAMPLE_LIMIT, LEVEL0_PARALLEL, WORKERS


# Tortilla parameters
PAD_TO = None
STRICT_SCHEMA = True


{% if cookiecutter.max_levels|int == 0 %}# Sample builders - one function per file type
def build_sample_rgb(ctx: dict) -> Sample:
    """RGB image (3 bands, uint8)"""
    sample = Sample(id="rgb", path=b"/path/to/rgb.tif")
    # sample.extend_with(Header())
    # sample.extend_with(GeotiffStats())
    # sample.extend_with(CustomMetadata(region="north", quality_score=0.95))
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
{% else %}# Sample builders - one function per root folder
def build_sample_tile(ctx: dict) -> Sample:
    """Tile FOLDER sample wrapping level1 Tortilla."""
    child_tortilla = level1.build(ctx)
    sample = Sample(id=ctx["id"], path=child_tortilla)
    # sample.extend_with(CustomMetadata(region="Valencia", quality_score=0.95))
    return sample


SAMPLES = [
    build_sample_tile,
]
{% endif %}

# Helper for parallel processing - must be at module level for pickling
def _build_samples_parallel(ctx: dict) -> tuple[list[Sample] | None, tuple[str, str] | None]:
    """
    Build samples for one context (used in parallel mode).
    
    Returns:
        (samples, None) on success
        (None, (id, error)) on failure
    """
    try:
        return [fn(ctx) for fn in SAMPLES], None
    except Exception as e:
        return None, (ctx["id"], str(e))


# Build function - ROOT level iterates over ALL contexts
def build(contexts: list[dict] | None = None, parallel: bool | None = None, workers: int | None = None) -> Tortilla:
    """
    Build root Tortilla from contexts.
    
    Args:
        contexts: List of context dicts, if None uses load_contexts(LEVEL0_SAMPLE_LIMIT)
        parallel: Enable parallel processing, if None uses LEVEL0_PARALLEL from config
        workers: Number of workers, if None uses WORKERS from config
    """
    if contexts is None:
        contexts = load_contexts(limit=LEVEL0_SAMPLE_LIMIT)
    
    if parallel is None:
        parallel = LEVEL0_PARALLEL
    
    if workers is None:
        workers = WORKERS
    
    failed_ids = []
    
    # Generate samples in parallel or serial
    if parallel:
        from concurrent.futures import ProcessPoolExecutor
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(_build_samples_parallel, contexts))
        
        samples = []
        for result, error in results:
            if error:
                failed_ids.append(error[0])
                print(f"Failed to build sample {error[0]}: {error[1]}")
            else:
                samples.extend(result)
    else:
        samples = []
        for ctx in contexts:
            try:
                samples.extend([fn(ctx) for fn in SAMPLES])
            except Exception as e:
                failed_ids.append(ctx["id"])
                print(f"Failed to build sample {ctx['id']}: {e}")
    
    if failed_ids:
        print(f"\nTotal failed samples: {len(failed_ids)}")
        print(f"Failed IDs: {failed_ids}")
    
    return Tortilla(
        samples=samples,
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA,
    )


# Validation - run directly to test
if __name__ == "__main__":
{% if cookiecutter.max_levels|int > 0 %}    import importlib
    importlib.reload(level1)
{% endif %}
    contexts = load_contexts(limit=LEVEL0_SAMPLE_LIMIT or 2)
    print(f"Building level0 with {len(contexts)} contexts...")
    print(f"Parallel: {LEVEL0_PARALLEL}, Workers: {WORKERS}")
    tortilla = build(contexts)
    print(f"Created {len(tortilla.samples)} root samples")
    print(tortilla.export_metadata())