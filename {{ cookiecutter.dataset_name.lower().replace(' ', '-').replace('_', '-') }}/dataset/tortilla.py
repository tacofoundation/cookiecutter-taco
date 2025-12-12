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

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pyarrow as pa
from tacotoolbox.datamodel import Tortilla
from tacotoolbox.tortilla.datamodel import TortillaExtension
from dataset.levels import level0


# Mock Tortilla Extension
# Demonstrates how to create extensions that compute metadata across all samples.
# Real extensions like MajorTOM require stac:centroid from STAC extension.

class MockTortillaExtension(TortillaExtension):
    """
    Example extension that adds computed metadata to all samples.
    
    This is a simple demonstration. Real extensions can compute:
    - Spatial groupings (MajorTOM, SpatialGrouping)
    - Statistics across samples
    - Earth Engine enrichment (GeoEnrich)
    """
    
    prefix: str = "sample"
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([
            pa.field("mock:label", pa.string()),
            pa.field("mock:index", pa.int32()),
        ])
    
    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "mock:label": "Sample label with prefix",
            "mock:index": "Sample index in tortilla",
        }
    
    def _compute(self, tortilla: Tortilla) -> pa.Table:
        n = len(tortilla.samples)
        return pa.Table.from_pydict({
            "mock:label": [f"{self.prefix}_{i:04d}" for i in range(n)],
            "mock:index": list(range(n)),
        }, schema=self.get_schema())


def create_tortilla(contexts: list[dict] | None = None) -> Tortilla:
    """
    Build root Tortilla from level0.
    
    Args:
        contexts: List of context dicts. If None, level0 uses MOCK_CONTEXTS.
    
    Returns:
        Tortilla: Root tortilla with extensions applied
    """
    print("Building root Tortilla...")
    root_tortilla = level0.build(contexts)
    
    # Tortilla extensions
    # Add computed metadata across all samples.
    # 
    # Mock extension (always works):
    root_tortilla.extend_with(MockTortillaExtension(prefix="root"))
    
    # Real extensions (require stac:centroid from STAC extension):
    # from tacotoolbox.tortilla.extensions.majortom import MajorTOM
    # root_tortilla.extend_with(MajorTOM(dist_km=100))
    #
    # from tacotoolbox.tortilla.extensions.spatial_grouping import SpatialGrouping
    # root_tortilla.extend_with(SpatialGrouping(target_count=1000))
    #
    # from tacotoolbox.tortilla.extensions.geoenrich import GeoEnrich
    # root_tortilla.extend_with(GeoEnrich(variables=["elevation", "temperature"]))
    
    return root_tortilla


if __name__ == "__main__":
    import importlib
    importlib.reload(level0)
    
    print("Creating root Tortilla with mocks...")
    tortilla = create_tortilla()
    print(f"Created {len(tortilla.samples)} root samples")
    print(tortilla.export_metadata())