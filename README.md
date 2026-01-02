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
pip install tacotoolbox[docs] tacoreader
```

## Generated Structure

```
my-dataset/
├── requirements.txt
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

1. Edit `config.py` → set metadata (title, description, license, etc.)
2. Edit `metadata.py` → implement `load_contexts()` to load your data
3. Edit `levels/*.py` → define how samples are built
4. Run `python -m dataset.create` → generates `.tacozip` + docs

Optional (only if adding custom extensions):
- Edit `extensions.py` → define custom extensions
- Edit `tortilla.py` → add Tortilla-level extensions (MajorTOM, SpatialGrouping, etc.)
- Edit `taco.py` → add TACO-level extensions (Publications, etc.)

## Test Before Building

```bash
python -m dataset.levels.level0   # Test root level
python -m dataset.tortilla        # Test complete structure
python -m dataset.taco            # Preview COLLECTION.json
```

## Documentation

- [TacoToolbox](https://github.com/tacofoundation/tacotoolbox) - Full documentation on creating datasets
- [TacoReader](https://github.com/tacofoundation/tacoreader) - Query and read TACO datasets
- [Specification](https://tacofoundation.github.io/specification) - TACO format spec

## License

MIT