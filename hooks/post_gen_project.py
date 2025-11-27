"""Post-generation hook to clean up unnecessary level files."""
import os

max_levels = int('{{ cookiecutter.max_levels }}')

# Remove level files beyond max_levels silently
for level in range(max_levels + 1, 5):
    level_file = f'dataset/levels/level{level}.py'
    if os.path.exists(level_file):
        os.remove(level_file)