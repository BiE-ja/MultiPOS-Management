import os
import importlib

# Chemin absolu du dossier actuel (app/models)
package_dir = os.path.dirname(__file__)

# Parcours tous les .py (sauf __init__.py et fichiers cachés)
for filename in os.listdir(package_dir):
    if filename.endswith(".py") and not filename.startswith("_") and filename != "__init__.py":
        module_name = filename[:-3]  # enleve ".py"
        importlib.import_module(f"{__name__}.{module_name}")