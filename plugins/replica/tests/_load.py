"""Load a script from a skill folder (the folder names have hyphens)."""

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(folder, name):
    # [V2H] No catálogo, as pastas replica-<x>/ do upstream vivem em skills/<x>/.
    path = os.path.join(ROOT, "skills", folder.replace("replica-", "", 1), name + ".py")
    spec = importlib.util.spec_from_file_location("replica_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
