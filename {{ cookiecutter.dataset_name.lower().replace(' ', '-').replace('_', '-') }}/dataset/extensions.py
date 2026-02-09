"""
Dataset Extensions

Extensions add metadata to your TACO dataset at different levels:

1. SampleExtension - Per-file or per-folder metadata
   Applied in levelN.py: sample.extend_with(MyExtension(...))
   
2. TortillaExtension - Computed across all samples in a tortilla
   Applied in tortilla.py: tortilla.extend_with(MyExtension())
   
3. TacoExtension - Dataset-wide metadata
   Applied in taco.py: taco.extend_with(MyExtension())

Each extension must implement 3 methods:
- get_schema() -> pa.Schema with field names + types
- get_field_descriptions() -> dict mapping field name to description
- _compute() -> pa.Table with the actual metadata values
"""

import pyarrow as pa
from tacotoolbox.sample.datamodel import SampleExtension
from tacotoolbox.tortilla.datamodel import TortillaExtension
from tacotoolbox.taco.datamodel import TacoExtension


class CustomMetadata(SampleExtension):
    """
    Example SampleExtension that adds custom metadata to each sample.
    
    Fields are passed when calling the extension:
        sample.extend_with(CustomMetadata(region="north", quality_score=0.95))
    """

    # Define your fields here (these come from your context or computed)
    region: str
    quality_score: float
    flag: str | None = None

    def get_schema(self) -> pa.Schema:
        """
        Define the PyArrow schema for this extension.
        
        Field names should use prefix pattern: "namespace:fieldname"
        """
        return pa.schema([
            pa.field("custom:region", pa.string()),
            pa.field("custom:quality_score", pa.float32()),
            pa.field("custom:flag", pa.string()),
        ])

    def get_field_descriptions(self) -> dict[str, str]:
        """
        Human-readable descriptions for documentation.
        
        These appear in COLLECTION.json and generated docs.
        """
        return {
            "custom:region": "Geographic region",
            "custom:quality_score": "Quality assessment score (0-1)",
            "custom:flag": "Optional processing flag",
        }

    def _compute(self, sample) -> pa.Table:
        """
        Generate the actual metadata values as a PyArrow Table.
        
        Args:
            sample: The Sample object this extension is attached to
            
        Returns:
            PyArrow Table with one row containing the metadata
        """
        return pa.table(
            {
                "custom:region": [self.region],
                "custom:quality_score": [self.quality_score],
                "custom:flag": [self.flag],
            },
            schema=self.get_schema(),
        )


class GeometryExtension(SampleExtension):
    """
    Example: Convert WKT geometry to WKB binary format.
    
    WKB (Well-Known Binary) is more efficient for storage than WKT strings.
    """

    wkt: str  # Input as WKT string
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([pa.field("geometry:wkb", pa.binary())])

    def get_field_descriptions(self) -> dict[str, str]:
        return {"geometry:wkb": "Geometry in WKB binary format"}

    def _compute(self, sample) -> pa.Table:
        import geopandas as gpd
        
        wkb = gpd.GeoSeries.from_wkt([self.wkt]).to_wkb()[0]
        return pa.table(
            {"geometry:wkb": [wkb]},
            schema=self.get_schema(),
        )


class SpatialCoverage(TortillaExtension):
    """
    Example TortillaExtension that computes statistics across all samples.
    
    TortillaExtensions don't take initialization parameters.
    They compute metadata from the entire tortilla.
    """
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([
            pa.field("coverage:n_samples", pa.int64()),
            pa.field("coverage:total_area", pa.float32()),
        ])

    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "coverage:n_samples": "Total number of samples",
            "coverage:total_area": "Total coverage area in km²",
        }

    def _compute(self, tortilla) -> pa.Table:
        """
        Compute metadata from all samples in the tortilla.
        
        IMPORTANT: Must return a table with N rows (one per sample),
        not a single-row summary. TortillaExtensions add columns to
        the existing metadata table.
        
        Args:
            tortilla: The Tortilla object containing all samples
        """
        n_samples = len(tortilla.samples)
        
        # Example: same value for all rows (broadcast)
        # For per-sample values, compute individually
        total_area = 0.0
        # TODO: Extract geometries from samples and sum areas

        return pa.table(
            {
                "coverage:n_samples": [n_samples] * n_samples,
                "coverage:total_area": [total_area] * n_samples,
            },
            schema=self.get_schema(),
        )


class DatasetStats(TacoExtension):
    """
    Example TacoExtension for dataset-wide metadata.
    
    TacoExtensions compute metadata for the entire TACO dataset.
    Must return a single-row table.
    """
    
    def get_schema(self) -> pa.Schema:
        return pa.schema([
            pa.field("stats:creation_date", pa.string()),
            pa.field("stats:n_root_samples", pa.int64()),
        ])

    def get_field_descriptions(self) -> dict[str, str]:
        return {
            "stats:creation_date": "ISO timestamp when dataset was created",
            "stats:n_root_samples": "Number of root-level samples",
        }

    def _compute(self, taco) -> pa.Table:
        """
        Compute dataset-wide metadata.
        
        Args:
            taco: The complete Taco object
            
        Returns:
            PyArrow Table with ONE row containing dataset statistics
        """
        from datetime import datetime
        
        return pa.table(
            {
                "stats:creation_date": [datetime.now().isoformat()],
                "stats:n_root_samples": [len(taco.tortilla.samples)],
            },
            schema=self.get_schema(),
        )