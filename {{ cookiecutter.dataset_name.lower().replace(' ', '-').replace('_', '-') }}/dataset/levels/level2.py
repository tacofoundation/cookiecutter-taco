"""
Level 2{% if cookiecutter.max_levels|int == 2 %} - Leaf Level{% endif %}

{% if cookiecutter.max_levels|int == 2 %}This is the LEAF level of your TACO hierarchy. Each sample here is a FILE
(the actual data), not a FOLDER containing more samples.

Structure:
- level0 (root) → level1 → level2 (LEAF - FILEs)
- level2 samples are FILEs with actual data (GeoTIFF, PNG, bytes, etc.)
{% else %}This is the THIRD level of your TACO hierarchy. Each sample here is contained
within a level1 sample.

Structure:
- level0 (root) → level1 → level2 (this level) → ... → level{{ cookiecutter.max_levels }} (leaves)
- level2 samples are FOLDERs that contain level3 tortillas
{% endif %}

How to use:
{% if cookiecutter.max_levels|int == 2 %}1. Copy build_sample_example() and rename it (e.g., build_sample_image_001)
2. Implement your logic to create/load the actual file data
3. Return Sample with path pointing to file data (bytes, Path, or file object)
4. Add the function to the SAMPLES list
5. Repeat for all files at this level
{% else %}1. Copy build_sample_example() and rename it (e.g., build_sample_scene_001)
2. Implement your logic to build the child tortilla from level3
3. Add the function to the SAMPLES list
4. Repeat for all samples at this level
{% endif %}

Note:
    level1-N builds are always SEQUENTIAL (no parallelism) to avoid nested
    parallelism issues. Only level0 can be parallel (controlled in config.py).
"""

from tacotoolbox.datamodel import Sample, Tortilla
{% if cookiecutter.max_levels|int > 2 %}from dataset.levels import level3{% endif %}

# =============================================================================
# TORTILLA PARAMETERS
# =============================================================================

PAD_TO = None
STRICT_SCHEMA = True


# =============================================================================
# SAMPLE BUILDERS - TODO: IMPLEMENT YOUR SAMPLES HERE
# =============================================================================
{% if cookiecutter.max_levels|int == 2 %}# Each function builds ONE FILE sample at this level.
{% else %}# Each function builds ONE sample at this level.
{% endif %}


def build_sample_example() -> Sample:
    """TODO: Rename and implement this function for your first sample."""
{% if cookiecutter.max_levels|int == 2 %}    data = b"test_data"
    sample = Sample(id="example", path=data)
{% else %}    child_tortilla = level3.build()
    sample = Sample(id="example", path=child_tortilla)
{% endif %}    
    # =========================================================================
    # ADD YOUR SAMPLE-LEVEL EXTENSIONS HERE
    # =========================================================================
{% if cookiecutter.max_levels|int == 2 %}    # LEAF level: add file-specific extensions
    # from extensions.geotiff_stats import GeotiffStats
    # sample.extend_with(GeotiffStats(categorical=False))
{% else %}    # from extensions.stac import STAC
    # sample.extend_with(STAC(...))
{% endif %}    # =========================================================================
    
    return sample


# =============================================================================
# SAMPLES LIST
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
# VALIDATION
# =============================================================================

if __name__ == "__main__":
    from levels import validate
    
    print("Running level2 validation...")    
    validate(SAMPLES, sample_ratio=1.0, workers=2)
    
    print("\nBuilding tortilla...")
    tortilla = build()
    print(f"Success! Created {len(tortilla.samples)} samples")