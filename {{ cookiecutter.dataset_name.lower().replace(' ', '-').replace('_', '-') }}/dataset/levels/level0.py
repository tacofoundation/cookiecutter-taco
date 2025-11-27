"""
Level 0 - Root Level

This is the ROOT level of your TACO hierarchy. Each sample here becomes a
top-level entry in your dataset.

Structure:
- level0 samples are FOLDERs that contain level1 tortillas
- level1 → level2 → ... → level{{ cookiecutter.max_levels }} (leaves are FILEs)

How to use:
1. Copy build_sample_example() and rename it (e.g., build_sample_tile_001)
2. Implement your logic to build the child tortilla from level1
3. Add the function to the SAMPLES list
4. Repeat for all root samples in your dataset

Note:
    level0 can be built in parallel (controlled by LEVEL0_PARALLEL in config.py).
    All other levels (level1-N) are always sequential to avoid nested parallelism.
"""

from concurrent.futures import ProcessPoolExecutor
from tacotoolbox.datamodel import Sample, Tortilla
from tqdm import tqdm
from dataset.config import LEVEL0_PARALLEL, LEVEL0_SAMPLE_LIMIT, WORKERS
from dataset.levels import level1

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
# Each function builds ONE root sample.
# Copy, rename, and modify build_sample_example() for each sample in your dataset.


def build_sample_example() -> Sample:
    """TODO: Rename and implement this function for your first sample."""
    child_tortilla = level1.build()
    
    sample = Sample(id="example", path=child_tortilla)
    
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
    #
    #   from extensions.istac import ISTAC
    #   sample.extend_with(ISTAC(
    #       crs="EPSG:4326",
    #       geometry=wkb_bytes,
    #       time_start=1609459200
    #   ))
    #
    #   from extensions.split import Split
    #   sample.extend_with(Split(split="train"))
    #
    # =========================================================================
    
    return sample


# =============================================================================
# SAMPLES LIST - Add all your sample builder functions here
# =============================================================================
# This list will be processed in parallel by tortilla.py

SAMPLES = [build_sample_example]


# =============================================================================
# BUILD FUNCTION - Infrastructure (DO NOT EDIT)
# =============================================================================


def _call_sample_builder(fn):
    """Helper to call sample builder function."""
    return fn()


def build() -> Tortilla:
    """
    Build Tortilla from all samples in SAMPLES list.
    
    Uses parallel processing if LEVEL0_PARALLEL=True in config.py.
    Respects LEVEL0_SAMPLE_LIMIT for debugging (None = build all samples).
    """
    # Apply sample limit if configured
    samples_to_build = SAMPLES[:LEVEL0_SAMPLE_LIMIT] if LEVEL0_SAMPLE_LIMIT else SAMPLES
    
    if LEVEL0_SAMPLE_LIMIT:
        print(f"DEBUG MODE: Building only {len(samples_to_build)}/{len(SAMPLES)} samples")
    
    if LEVEL0_PARALLEL:
        # Parallel execution (default)
        with ProcessPoolExecutor(max_workers=WORKERS) as pool:
            samples = list(tqdm(
                pool.map(_call_sample_builder, samples_to_build),
                total=len(samples_to_build),
                desc="Building level0"
            ))
    else:
        # Sequential execution (debugging)
        samples = [fn() for fn in tqdm(samples_to_build, desc="Building level0")]
    
    return Tortilla(
        samples=samples,
        pad_to=PAD_TO,
        strict_schema=STRICT_SCHEMA
    )


# =============================================================================
# VALIDATION - Run this file directly to test your samples
# =============================================================================

if __name__ == "__main__":
    from levels import validate
    
    print("Running level0 validation...")    
    validate(SAMPLES, sample_ratio=1.0, workers=2)
    
    print("\nBuilding tortilla...")
    tortilla = build()
    print(f"Success! Created {len(tortilla.samples)} samples")