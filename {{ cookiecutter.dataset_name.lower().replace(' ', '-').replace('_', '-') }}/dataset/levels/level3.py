"""
Level 3{% if cookiecutter.max_levels|int == 3 %} - Leaf Level{% endif %}

{% if cookiecutter.max_levels|int == 3 %}This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
- level0 (root) → level1 → level2 → level3 (LEAF - FILEs)
- level3 samples are FILEs with actual data (GeoTIFF, PNG, bytes, etc.)
{% else %}This is the FOURTH level of your TACO hierarchy. Each sample here is contained
within a level2 sample.

Structure:
- level0 (root) → level1 → level2 → level3 (this level) → level4 (leaves)
- level3 samples are FOLDERs that contain level4 tortillas
{% endif %}

How to use:
{% if cookiecutter.max_levels|int == 3 %}1. Copy build_sample_example() and rename it (e.g., build_sample_image_001)
2. Implement your logic to create/load the actual file data
3. Return Sample with path pointing to file data (bytes, Path, or file object)
4. Add the function to the SAMPLES list
5. Repeat for all files at this level
{% else %}1. Copy build_sample_example() and rename it (e.g., build_sample_band_001)
2. Implement your logic to build the child tortilla from level4
3. Add the function to the SAMPLES list
4. Repeat for all samples at this level
{% endif %}

Note:
    level1-N builds are always SEQUENTIAL (no parallelism) to avoid nested
    parallelism issues. Only level0 can be parallel (controlled in config.py).
"""

from tacotoolbox.datamodel import Sample, Tortilla
{% if cookiecutter.max_levels|int > 3 %}from dataset.levels import level4{% endif %}

# =============================================================================
# TORTILLA PARAMETERS
# =============================================================================

# PAD_TO: Auto-pad samples to make count divisible by this number
#   None = no padding (default)
#   Example: PAD_TO = 10 pads [1,2,3] -> [1,2,3,PAD,PAD,PAD,PAD,PAD,PAD,PAD]
PAD_TO = None

# STRICT_SCHEMA: Enforce uniform metadata schema across all samples
#   True = all samples MUST have identical metadata fields (recommended)
#   False = heterogeneous schemas allowed, missing fields filled with None
STRICT_SCHEMA = True


# =============================================================================
# SAMPLE BUILDERS - TODO: IMPLEMENT YOUR SAMPLES HERE
# =============================================================================
{% if cookiecutter.max_levels|int == 3 %}# Each function builds ONE FILE sample at this level.
# Copy, rename, and modify build_sample_example() for each file.
{% else %}# Each function builds ONE sample at this level.
# Copy, rename, and modify build_sample_example() for each sample.
{% endif %}


def build_sample_example() -> Sample:
    """TODO: Rename and implement this function for your first sample."""
{% if cookiecutter.max_levels|int == 3 %}    # Example: Create in-memory data
    data = b"test_data"
    
    sample = Sample(id="example", path=data)
{% else %}    child_tortilla = level4.build()
    
    sample = Sample(id="example", path=child_tortilla)
{% endif %}    
    # =========================================================================
    # ADD YOUR SAMPLE-LEVEL EXTENSIONS HERE
    # =========================================================================
    # Sample extensions add metadata to individual samples.
    #
    # Examples (based on available extensions):
    #
    #   from extensions.stac import STAC
    #   sample.extend_with(STAC(
    #       crs="EPSG:4326",
    #       tensor_shape=(256, 256),
    #       geotransform=(0, 1, 0, 0, 0, -1),
    #       time_start=1609459200
    #   ))
{% if cookiecutter.max_levels|int == 3 %}    #
    #   from extensions.scaling import Scaling
    #   sample.extend_with(Scaling(
    #       scale_factor=0.0001,
    #       scale_offset=0.0
    #   ))
    #
    #   from extensions.geotiff_stats import GeotiffStats
    #   sample.extend_with(GeotiffStats(categorical=False))
{% endif %}    #
    #   from extensions.split import Split
    #   sample.extend_with(Split(split="train"))
    #
    # =========================================================================
    
    return sample


# =============================================================================
# SAMPLES LIST - Add all your sample builder functions here
# =============================================================================

SAMPLES = [build_sample_example]


# =============================================================================
# BUILD FUNCTION - Infrastructure (DO NOT EDIT)
# =============================================================================


def build() -> Tortilla:
    """Build Tortilla from all samples in SAMPLES list (sequential)."""
    return Tortilla(
        samples=[fn() for fn in SAMPLES],
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA
    )


# =============================================================================
# VALIDATION - Run this file directly to test your samples
# =============================================================================

if __name__ == "__main__":
    from levels import validate
    
    print("Running level3 validation...")    
    validate(SAMPLES, sample_ratio=1.0, workers=2)
    
    print("\nBuilding tortilla...")
    tortilla = build()
    print(f"Success! Created {len(tortilla.samples)} samples")