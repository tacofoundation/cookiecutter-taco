"""
Root Tortilla Definition

This module creates the root Tortilla by:
1. Calling level0.build() to get all root samples
2. Optionally applying Tortilla-level extensions

Tortilla-level extensions add metadata columns computed across ALL samples:
- MajorTOM: spherical grid codes (requires stac:centroid)
- SpatialGrouping: groups by spatial proximity (requires stac:centroid)
- GeoEnrich: Earth Engine data enrichment (requires stac:centroid)
- Custom extensions: any computed metadata

Run directly to test:
    python dataset/tortilla.py
"""

from tacotoolbox.datamodel import Tortilla
# from tacotoolbox.tortilla.extensions.majortom import MajorTOM
# from tacotoolbox.tortilla.extensions.spatial_grouping import SpatialGrouping
# from tacotoolbox.tortilla.extensions.geoenrich import GeoEnrich
# from dataset.extensions import SpatialCoverage

from dataset.levels import level0
from dataset.metadata import load_contexts
from dataset.config import LEVEL0_SAMPLE_LIMIT, LEVEL0_PARALLEL, WORKERS


def create_tortilla(contexts: list[dict] | None = None, parallel: bool | None = None, workers: int | None = None) -> Tortilla:
    """
    Build root Tortilla from level0.
    
    Args:
        contexts: List of context dicts, if None uses load_contexts(LEVEL0_SAMPLE_LIMIT)
        parallel: Enable parallel processing, if None uses LEVEL0_PARALLEL from config
        workers: Number of workers, if None uses WORKERS from config
    
    Returns:
        Tortilla: Root tortilla with extensions applied
    """
    if contexts is None:
        contexts = load_contexts(limit=LEVEL0_SAMPLE_LIMIT)
    
    if parallel is None:
        parallel = LEVEL0_PARALLEL
    
    if workers is None:
        workers = WORKERS
    
    print(f"Building root Tortilla with {len(contexts)} contexts...")
    print(f"Parallel: {parallel}, Workers: {workers}")
    
    root_tortilla = level0.build(contexts, parallel=parallel, workers=workers)
    
    # Tortilla extensions - computed metadata across all samples
    # Uncomment extensions as needed:
    
    # root_tortilla.extend_with(SpatialCoverage())
    # root_tortilla.extend_with(MajorTOM(dist_km=100))
    # root_tortilla.extend_with(SpatialGrouping(target_count=1000))
    # root_tortilla.extend_with(GeoEnrich(variables=["elevation", "temperature"]))
    
    return root_tortilla


if __name__ == "__main__":
    import importlib
    importlib.reload(level0)
    
    contexts = load_contexts(limit=LEVEL0_SAMPLE_LIMIT or 2)
    print(f"Creating root Tortilla...")
    tortilla = create_tortilla(contexts)
    print(f"Created {len(tortilla.samples)} root samples")
    print(tortilla.export_metadata())