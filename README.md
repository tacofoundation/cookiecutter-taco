# cookiecutter-taco

Cookiecutter template for creating [TACO](https://tacofoundation.github.io/specification) datasets.

## Quick Start

```bash
pip install cookiecutter
cookiecutter gh:tacofoundation/cookiecutter-taco
```

You'll be asked:
- `dataset_name`: Your dataset identifier (e.g., `my-dataset`)
- `max_levels`: Hierarchy depth (0-4)

Then:
```bash
cd my-dataset
pip install tacotoolbox[docs]
```

## Requirements

- Python >= 3.10
- tacotoolbox >= 0.25.0
- GDAL (only for GeoTIFF processing)

Optional:
- tacoreader >= 2.3.0 (only if loading metadata from existing TACO datasets)

## Generated Structure

```
my-dataset/
└── dataset/
    ├── config.py       # Metadata + build settings
    ├── metadata.py     # Load your data sources
    ├── extensions.py   # Custom extensions (optional)
    ├── create.py       # Build script (don't edit)
    ├── taco.py         # TACO assembly
    ├── tortilla.py     # Root tortilla
    └── levels/
        ├── level0.py   # Root samples
        └── ...         # Child levels
```

## Workflow

1. Edit `config.py` -> set metadata (title, description, license, etc.)
2. Edit `metadata.py` -> implement `load_contexts()` to load your data
3. Edit `levels/*.py` -> define how samples are built (bottom-up, start from leaf level)
4. Run `python -m dataset.create` -> generates `.tacozip` + docs

Optional:
- Edit `extensions.py` -> define custom extensions
- Edit `tortilla.py` -> add Tortilla-level extensions (MajorTOM, GeoEnrich)
- Edit `taco.py` -> add TACO-level extensions (Publications, Labels, OpticalData)

## Contexts

A context is a dict with everything needed to build one root sample. You define how to load them in `metadata.py` by implementing `load_contexts()`. The only required field is `"id"`, the rest depends on what your levels need.

```python
# metadata.py
def load_contexts(limit=None):
    return [
        {"id": "tile_001", "image": "/data/tile_001/rgb.tif", "mask": "/data/tile_001/label.tif"},
        {"id": "tile_002", "image": "/data/tile_002/rgb.tif", "mask": "/data/tile_002/label.tif"},
    ]
```

Contexts flow through the hierarchy: `level0` iterates over all of them, then passes each one down to `level1 -> level2 -> ... -> leaf`, where the actual `Sample` objects are created using the context fields.

```
load_contexts() -> [ctx, ctx, ctx, ...]
                        |
                   level0.build(contexts)       # iterates ALL contexts
                        |
                   level1.build(ctx)            # ONE context
                        |
                   Sample(id="rgb", path=ctx["image"].encode())
```

Sources: CSV, Parquet, filesystem scan, database, API, or existing TACO datasets via tacoreader.

## Test Before Building

Test each level independently, bottom-up:

```bash
python -m dataset.levels.level1   # Test leaf level first
python -m dataset.levels.level0   # Test root level
python -m dataset.tortilla        # Test complete structure
python -m dataset.taco            # Preview COLLECTION.json
python -m dataset.create          # Full build
```

## Available Extensions

### Sample-level (in levels/*.py)

```python
from tacotoolbox.sample.extensions.tacotiff import Header
from tacotoolbox.sample.extensions.geotiff_stats import GeotiffStats
from tacotoolbox.sample.extensions.stac import STAC
from tacotoolbox.sample.extensions.istac import ISTAC
from tacotoolbox.sample.extensions.scaling import Scaling
from tacotoolbox.sample.extensions.split import Split
```

### Tortilla-level (in tortilla.py)

```python
from tacotoolbox.tortilla.extensions.majortom import MajorTOM
from tacotoolbox.tortilla.extensions.geoenrich import GeoEnrich
```

### TACO-level (in taco.py)

```python
from tacotoolbox.taco.extensions.scientific import Publication, Publications
from tacotoolbox.taco.extensions.labels import Labels, LabelClass
from tacotoolbox.taco.extensions.opticaldata import OpticalData, SpectralBand
from tacotoolbox.taco.extensions.split import SplitStrategy, SplitStrategyType
```

## Documentation

- [TacoToolbox](https://github.com/tacofoundation/tacotoolbox) - Creating datasets
- [TacoReader](https://github.com/tacofoundation/tacoreader) - Query and read datasets
- [TacoBridge](https://github.com/tacofoundation/tacobridge) - Export and convert datasets
- [Specification](https://tacofoundation.github.io/specification) - TACO format spec

## License

MIT