"""
Metadata Provider

This module loads your dataset metadata and provides it as contexts.

A "context" is a dict containing all information needed to build one root sample.
- REQUIRED: "id" field (unique identifier)
- OPTIONAL: any other fields your levels need (paths, coordinates, dates, etc.)

How contexts flow through TACO:
1. load_contexts() returns list[dict]
2. level0.build() iterates over all contexts
3. Each context is passed to level1.build() → level2.build() → ... → leaf level
4. Levels use context fields to locate files, apply extensions, build samples

The limit parameter enables testing with a subset of your data.

Usage:
    from dataset.metadata import load_contexts

    # Load all contexts
    contexts = load_contexts()

    # Load 10% for testing
    contexts = load_contexts(limit=0.1)

    # Load first 10 for testing
    contexts = load_contexts(limit=10)
"""


def load_contexts(limit: float | int | None = None) -> list[dict]:
    """
    Load dataset metadata and return list of context dicts.

    CUSTOMIZE THIS FUNCTION to match your data source.
    You can load from CSV, Parquet, filesystem, database, API, or any source.

    Args:
        limit: Optional limit for contexts
               - If None: returns all contexts
               - If float (0.0-1.0): percentage of total (e.g., 0.1 = 10%)
               - If int: exact count (e.g., 10 = first 10 contexts)

    Returns:
        list[dict]: One dict per root sample

        Each dict MUST have:
        - "id": str - unique identifier for this sample

        Each dict CAN have:
        - "path": bytes or str - location of data files
        - "date": str - acquisition date
        - "region": str - geographic region
        - "split": str - train/val/test partition
        - Any other fields your levels need
 
    Example return:
        [
            {
                "id": "sample_001",
                "path": b"/data/sample_001",
                "date": "2024-01-15",
                "region": "valencia",
                "cloud_cover": 12.5
            },
            ...
        ]
    """
    
    # REPLACE THIS SECTION WITH YOUR DATA LOADING
    # 
    # Example 1: Load from CSV file
    # import polars as pl
    # df = pl.read_csv("metadata.csv")
    # if limit is not None:
    #     if isinstance(limit, float):
    #         count = int(len(df) * limit) or 1
    #         df = df.head(count)
    #     else:
    #         df = df.head(limit)
    # return df.to_dicts()

    # Example 2: Load from Parquet file
    # import polars as pl
    # df = pl.read_parquet("metadata.parquet")
    # if limit is not None:
    #     if isinstance(limit, float):
    #         count = int(len(df) * limit) or 1
    #         df = df.head(count)
    #     else:
    #         df = df.head(limit)
    # return df.to_dicts()

    # Example 3: Scan filesystem
    # from pathlib import Path
    # contexts = []
    # for folder in sorted(Path("data").iterdir()):
    #     contexts.append({
    #         "id": folder.name,
    #         "path": str(folder).encode()
    #     })
    # if limit is not None:
    #     if isinstance(limit, float):
    #         count = int(len(contexts) * limit) or 1
    #         return contexts[:count]
    #     else:
    #         return contexts[:limit]
    # return contexts

    # MOCK DATA (delete this when you add your implementation)

    contexts = [
        {"id": "sample01", "path": b"/mock/sample01"},
        {"id": "sample02", "path": b"/mock/sample02"},
        {"id": "sample03", "path": b"/mock/sample03"},
        {"id": "sample04", "path": b"/mock/sample04"},
        {"id": "sample05", "path": b"/mock/sample05"},
    ]
    
    if limit is None:
        return contexts
    elif isinstance(limit, float):
        # Percentage (0.0-1.0)
        count = int(len(contexts) * limit) or 1
        return contexts[:count]
    else:
        # Exact count
        return contexts[:limit]


if __name__ == "__main__":
    contexts = load_contexts()
    print(f"Loaded {len(contexts)} contexts")
    print(f"First context: {contexts[0]}")