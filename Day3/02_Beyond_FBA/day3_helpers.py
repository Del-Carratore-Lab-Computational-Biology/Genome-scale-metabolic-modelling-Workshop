"""Helpers for the CODE-M Day 3 notebooks.

You do not need to read this file to follow the notebooks. It provides:

* MODELS - the folder with the model files (../models);
* flux_map(fluxes, filename) - writes an Escher map of E. coli core fluxes to an
  HTML file you can open in a web browser. Escher is optional: if it isn't
  installed, the function says so and the notebook carries on.
"""
from pathlib import Path

MODELS = Path(__file__).resolve().parent.parent / "models"
ECOLI_CORE_MAP = MODELS / "e_coli_core.Core_metabolism.json"


def flux_map(fluxes, filename):
    """Write an Escher map of E. coli core `fluxes` (a dict or pandas Series) to `filename`."""
    try:
        import escher
    except Exception as err:          # not installed, or an incompatible version
        print(f"Escher is not available here ({type(err).__name__}): skipping the map.")
        return None
    builder = escher.Builder(map_json=str(ECOLI_CORE_MAP),
                             reaction_data={k: float(v) for k, v in dict(fluxes).items()})
    builder.save_html(filename)
    print(f"Map saved: open {filename} in a web browser (it needs internet to load Escher).")
    return filename
