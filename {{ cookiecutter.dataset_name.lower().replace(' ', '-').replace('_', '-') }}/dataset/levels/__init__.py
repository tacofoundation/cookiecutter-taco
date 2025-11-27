"""
TACO Hierarchy Levels

Validation utilities for testing sample builders before full dataset build.

Usage:
    from levels import validate, level0
    
    # Test 10% of samples with 4 workers
    validate(level0.SAMPLES, sample_ratio=0.1, workers=4)
    
    # Test all samples with 2 workers
    validate(level0.SAMPLES, sample_ratio=1.0, workers=2)
"""

import random
from typing import Callable
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm


def _validate_one(fn: Callable) -> str | None:
    """
    Execute a single sample builder function and catch errors.
    
    Returns:
        None if successful, error message string if failed
    """
    try:
        fn()
        return None
    except Exception as e:
        return f"{fn.__name__}: {e}"


def validate(
    samples: list[Callable],
    sample_ratio: float = 0.1,
    workers: int = 4
) -> bool:
    """
    Validate a subset of sample builder functions in parallel.
    
    Args:
        samples: List of sample builder functions (e.g., level0.SAMPLES)
        sample_ratio: Fraction of samples to test (0.0 to 1.0)
        workers: Number of parallel workers
        
    Returns:
        True if all tested samples passed, False if any errors
    """
    n_test = max(1, int(len(samples) * sample_ratio))
    test_samples = random.sample(samples, n_test)
    
    print(f"Testing {n_test}/{len(samples)} samples with {workers} workers...")
    
    errors = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(tqdm(
            pool.map(_validate_one, test_samples),
            total=len(test_samples)
        ))
        errors = [r for r in results if r is not None]
    
    if errors:
        print("Errors:\n" + "\n".join(f"  {e}" for e in errors))
        return False
    
    print("Validated!")
    return True