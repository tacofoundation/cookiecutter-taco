"""
Root Tortilla Definition

This module creates the root Tortilla by:
1. Building all root samples in parallel (from levels/level0.py)
2. Combining them into a Tortilla with uniform schema
3. Optionally applying Tortilla-level extensions

Tortilla-level extensions add metadata columns computed across all samples, such as:
- Geospatial metadata (MajorTOM, spatial grouping)
- Statistical aggregations (mean, std, percentiles)
- Earth Engine enrichment (GeoEnrich)
"""

from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

from tacotoolbox.datamodel import Tortilla

from dataset.config import BUILD_CONFIG
from dataset.levels import level0


def _call_sample_builder(fn):
    """Helper to call sample builder function."""
    return fn()


def create_tortilla() -> Tortilla:
    """
    Build all root samples and create root Tortilla.
    
    Samples are built in parallel using ProcessPoolExecutor with the number
    of workers specified in BUILD_CONFIG.
    
    Returns:
        Tortilla: Root tortilla with all samples and extensions applied
    """
    workers = BUILD_CONFIG.get("workers", 4)

    print(f"Building {len(level0.SAMPLES)} root samples with {workers} workers...")

    with ProcessPoolExecutor(max_workers=workers) as pool:
        root_samples = list(
            tqdm(
                pool.map(_call_sample_builder, level0.SAMPLES),
                total=len(level0.SAMPLES),
            )
        )

    print("Creating root Tortilla...")
    root_tortilla = Tortilla(samples=root_samples)

    # =========================================================================
    # ADD YOUR TORTILLA-LEVEL EXTENSIONS HERE
    # =========================================================================
    # Tortilla extensions add metadata columns computed across all samples.
    #
    # Examples (based on available extensions):
    #
    #   from extensions.majortom import MajorTOM
    #   root_tortilla.extend_with(MajorTOM(dist_km=100))
    #
    #   from extensions.spatial_grouping import SpatialGrouping
    #   root_tortilla.extend_with(SpatialGrouping(target_size=1000))
    #
    #   from extensions.geoenrich import GeoEnrich
    #   root_tortilla.extend_with(GeoEnrich(
    #       variables=["elevation", "temperature", "precipitation"],
    #       scale_m=5120.0
    #   ))
    #
    # =========================================================================

    return root_tortilla


if __name__ == "__main__":
    tortilla = create_tortilla()
    print(f"Created Tortilla with {len(tortilla.samples)} root samples")
    print("Success!")