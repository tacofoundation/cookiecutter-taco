"""
TACO Definition

This module creates the complete TACO dataset by:
1. Getting the root Tortilla (from tortilla.py)
2. Adding COLLECTION metadata (from config.py)
3. Optionally applying TACO-level extensions

TACO-level extensions add dataset-wide computed metadata, such as:
- Global statistics across all samples
- Dataset-wide spatial/temporal indices
- Provenance tracking or checksums
"""

from tacotoolbox.datamodel import Taco

from dataset.config import COLLECTION
from dataset.tortilla import create_tortilla


def create_taco() -> Taco:
    """
    Create TACO from root Tortilla + COLLECTION metadata.
    
    Returns:
        Taco: Complete dataset with collection metadata and extensions
    """
    # Get the root tortilla (with its extensions already applied)
    root_tortilla = create_tortilla()

    # Create TACO with collection metadata
    print("Creating TACO...")
    taco = Taco(tortilla=root_tortilla, **COLLECTION)

    # =========================================================================
    # ADD YOUR TACO-LEVEL EXTENSIONS HERE
    # =========================================================================
    # TACO extensions compute dataset-wide metadata.
    #
    # Example:
    #   from my_extensions import GlobalStatsExtension
    #   taco.extend_with(GlobalStatsExtension())
    #
    # Common use cases:
    # - Global statistics (min/max/mean across all samples)
    # - Dataset checksums or provenance tracking
    # - Spatial/temporal coverage summaries
    # =========================================================================

    return taco


if __name__ == "__main__":
    taco = create_taco()
    print(f"Created TACO: {taco.id} v{taco.dataset_version}")
    print(f"Root samples: {len(taco.tortilla.samples)}")
    print("Success!")