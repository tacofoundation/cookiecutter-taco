"""
TACO Dataset Definition

This is the final step to create your TACO dataset.

1. Calls create_tortilla() to get the root Tortilla
2. Wraps it in Taco with COLLECTION metadata (from config.py)
3. Applies TACO-level extensions (optional)

Run directly to test:
    python dataset/taco.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pyarrow as pa
from tacotoolbox.taco.datamodel import Taco, TacoExtension
from dataset.config import COLLECTION
from dataset.tortilla import create_tortilla


# Mock Taco Extension
# Demonstrates pattern for dataset-wide metadata

class MockTacoExtension(TacoExtension):
    """Example extension for dataset-wide metadata."""
    
    dataset_tag: str = "demo"
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([
            pa.field("mock:dataset_tag", pa.string()),
            pa.field("mock:total_samples", pa.int64()),
        ])
    
    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "mock:dataset_tag": "Demo tag for the dataset",
            "mock:total_samples": "Total number of samples in root tortilla",
        }
    
    def _compute(self, taco: Taco) -> pa.Table:
        n_samples = len(taco.tortilla.samples)
        return pa.Table.from_pydict({
            "mock:dataset_tag": [self.dataset_tag],
            "mock:total_samples": [n_samples],
        }, schema=self.get_schema())


def create_taco() -> Taco:
    """Create complete TACO from Tortilla + COLLECTION metadata."""
    print("Getting root Tortilla...")
    root_tortilla = create_tortilla()

    print("Creating TACO with COLLECTION metadata...")
    taco = Taco(tortilla=root_tortilla, **COLLECTION)

    # TACO-level extensions (optional)
    # Add dataset-wide metadata
    
    # Mock extension (always works):
    taco.extend_with(MockTacoExtension(dataset_tag="v1.0"))
    
    # Real extensions:
    # from tacotoolbox.taco.extensions.publications import Publications, Publication
    # taco.extend_with(Publications(publications=[
    #     Publication(
    #         doi="10.1038/s41586-021-03819-2",
    #         citation="Smith et al. (2023). Dataset Name. Nature.",
    #         summary="Introduces dataset methodology"
    #     )
    # ]))

    return taco


if __name__ == "__main__":
    print("Building complete TACO dataset...\n")
    
    taco = create_taco()
    
    print(f"\nTACO Created Successfully!")
    print(f"ID:              {taco.id}")
    print(f"Version:         {taco.dataset_version}")
    print(f"Root samples:    {len(taco.tortilla.samples)}")
    print(f"Tasks:           {', '.join(taco.tasks)}")
    
    print("\n✓ Ready to create dataset with: python dataset/build.py")