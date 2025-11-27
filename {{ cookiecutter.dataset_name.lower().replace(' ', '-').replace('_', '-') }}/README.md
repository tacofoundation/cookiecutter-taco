# {{ cookiecutter.dataset_name }}

TACO dataset built with [cookiecutter-taco](https://github.com/tacofoundation/cookiecutter-taco).

## Structure
```
{{ cookiecutter.dataset_name }}/
├── build.py                    # Build script
└── dataset/
    ├── config.py               # Metadata & build settings
    ├── taco.py                 # TACO assembly
    ├── tortilla.py             # Root tortilla
    └── levels/
        ├── __init__.py
        ├── level0.py           # Root level (parallel)
{% if cookiecutter.max_levels|int >= 1 %}        ├── level1.py{% endif %}
{% if cookiecutter.max_levels|int >= 2 %}        ├── level2.py{% endif %}
{% if cookiecutter.max_levels|int >= 3 %}        ├── level3.py{% endif %}
{% if cookiecutter.max_levels|int >= 4 %}        └── level4.py{% endif %}
```

## Hierarchy

This dataset has **{{ cookiecutter.max_levels|int + 1 }} levels**:

{% if cookiecutter.max_levels|int == 0 %}
```
level0 (root, FILES)
```
Root samples are files.
{% elif cookiecutter.max_levels|int == 1 %}
```
level0 (root, FOLDERS) → level1 (FILES)
```
Root samples contain level1 files.
{% elif cookiecutter.max_levels|int == 2 %}
```
level0 (root, FOLDERS) → level1 (FOLDERS) → level2 (FILES)
```
Two levels of folders before files.
{% elif cookiecutter.max_levels|int == 3 %}
```
level0 (root, FOLDERS) → level1 (FOLDERS) → level2 (FOLDERS) → level3 (FILES)
```
Three levels of folders before files.
{% elif cookiecutter.max_levels|int == 4 %}
```
level0 (root, FOLDERS) → level1 (FOLDERS) → level2 (FOLDERS) → level3 (FOLDERS) → level4 (FILES)
```
Four levels of folders before files.
{% endif %}

## Implementation Workflow

**1. Configure metadata** (`dataset/config.py`):
```python
COLLECTION_ID = "{{ cookiecutter.dataset_name }}"
COLLECTION_VERSION = "1.0.0"
COLLECTION_DESCRIPTION = "..."  # Edit this
WORKERS = 4
OUTPUT_PATH = "output.tacozip"
```

**2. Implement samples** (`dataset/levels/level*.py`):
```python
# Example for leaf level (files)
def build_sample_001() -> Sample:
    data = load_your_data()
    return Sample(id="001", path=data)

SAMPLES = [build_sample_001, ...]
```

**3. Test individual levels**:
```bash
python -m dataset.levels.level0
{% if cookiecutter.max_levels|int >= 1 %}python -m dataset.levels.level1{% endif %}
{% if cookiecutter.max_levels|int >= 2 %}python -m dataset.levels.level2{% endif %}
# ... test each level
```

**4. Build dataset**:
```bash
python build.py
```

Output: `output.tacozip` (or path from `OUTPUT_PATH`)

## Extensions

Add metadata extensions in `dataset/tortilla.py` or `dataset/taco.py`:
```python
# Tortilla-level (in tortilla.py)
from extensions.majortom import MajorTOM
root_tortilla.extend_with(MajorTOM(dist_km=100))

# Taco-level (in taco.py)
from my_extensions import GlobalStats
taco.extend_with(GlobalStats())
```

## Reading
```python
import tacoreader

# Load dataset
ds = tacoreader.load("output.tacozip")

# Query with SQL
df = ds.sql("SELECT * WHERE date > '2023-01-01'").data

# Access files
for vsi_path in df["internal:gdal_vsi"]:
    with rasterio.open(vsi_path) as src:
        data = src.read()
```

## Development
```bash
# Install dependencies
pip install tacotoolbox tacoreader

# Validate samples (10% sample, 4 workers)
from dataset.levels import validate, level0
validate(level0.SAMPLES, sample_ratio=0.1, workers=4)

# Debug mode (limit samples, disable parallelism)
# Edit dataset/config.py:
LEVEL0_SAMPLE_LIMIT = 10  # Build only 10 samples
LEVEL0_PARALLEL = False   # Sequential execution
```

## Resources

- [TACO Specification](https://tacofoundation.github.io/specification)
- [TacoToolbox](https://github.com/tacofoundation/tacotoolbox)
- [TacoReader](https://github.com/tacofoundation/tacoreader)

---

Generated with [cookiecutter-taco](https://github.com/tacofoundation/cookiecutter-taco)