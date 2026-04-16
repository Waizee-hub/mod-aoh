#!/usr/bin/env python3
"""
merge_with_game.py — Maritime Combat Units Mod installer
=========================================================

Ce script lit les vrais fichiers du jeu Age of History III, y injecte
les nouvelles unités navales et technologies du mod, puis écrit les
fichiers fusionnés directement dans le dossier du mod.

Utilisation
-----------
    python3 merge_with_game.py "<chemin vers le dossier du jeu>"

Exemples
--------
  Windows :
    python3 merge_with_game.py "C:/Program Files (x86)/Steam/steamapps/common/Age of History 3"

  macOS :
    python3 merge_with_game.py ~/Library/Application\ Support/Steam/steamapps/common/Age\ of\ History\ 3

  Linux :
    python3 merge_with_game.py ~/.steam/steam/steamapps/common/Age\ of\ History\ 3
"""

import json
import sys
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Chemins relatifs dans le jeu et dans le mod
# ---------------------------------------------------------------------------

UNITS_REL         = Path("game/units/Units.json")
TECHNOLOGIES_REL  = Path("game/technologies/Technologies.json")

MOD_ROOT = Path(__file__).parent


# ---------------------------------------------------------------------------
# Entrées que ce mod ajoute
# ---------------------------------------------------------------------------

MOD_UNIT_ENTRIES = [
    {"File": "Frigate.json",       "ID": 100, "Line": 0},
    {"File": "ShipOfTheLine.json", "ID": 101, "Line": 0},
    {"File": "Ironclad.json",      "ID": 102, "Line": 0},
    {"File": "Battleship.json",    "ID": 103, "Line": 0},
]

MOD_TECH_ENTRIES = [
    {"ID": 500, "Name": "NavalWarfare",           "ImageID": 500, "TreeColumn": 20, "TreeRow": 3, "RequiredTech": -1,  "RequiredTech2": -1, "BattleWidth": 0, "ResearchCost": 150,  "Repeatable": False, "AI": 3},
    {"ID": 501, "Name": "SteamPropulsion",        "ImageID": 501, "TreeColumn": 21, "TreeRow": 3, "RequiredTech": 500, "RequiredTech2": -1, "BattleWidth": 0, "ResearchCost": 280,  "Repeatable": False, "AI": 4},
    {"ID": 502, "Name": "IronHulls",              "ImageID": 502, "TreeColumn": 22, "TreeRow": 3, "RequiredTech": 501, "RequiredTech2": -1, "BattleWidth": 0, "ResearchCost": 450,  "Repeatable": False, "AI": 4},
    {"ID": 503, "Name": "SteelNavalEngineering",  "ImageID": 503, "TreeColumn": 23, "TreeRow": 3, "RequiredTech": 502, "RequiredTech2": -1, "BattleWidth": 2, "ResearchCost": 650,  "Repeatable": False, "AI": 5},
    {"ID": 504, "Name": "ModernNavalGunnery",     "ImageID": 504, "TreeColumn": 24, "TreeRow": 3, "RequiredTech": 503, "RequiredTech2": -1, "BattleWidth": 2, "ResearchCost": 900,  "Repeatable": False, "AI": 5},
    {"ID": 505, "Name": "NavalSupremacy",         "ImageID": 505, "TreeColumn": 25, "TreeRow": 3, "RequiredTech": 504, "RequiredTech2": -1, "BattleWidth": 4, "ResearchCost": 1300, "Repeatable": False, "AI": 6},
]

MOD_UNIT_IDS  = {e["ID"] for e in MOD_UNIT_ENTRIES}
MOD_TECH_IDS  = {e["ID"] for e in MOD_TECH_ENTRIES}


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Écrit : {path}")


def backup(path: Path):
    bak = path.with_suffix(".json.bak")
    if path.exists() and not bak.exists():
        shutil.copy2(path, bak)
        print(f"  Sauvegarde : {bak}")


def merge(base_list: list, mod_entries: list, id_key: str, mod_ids: set) -> list:
    """
    Fusionne base_list avec mod_entries.
    - Les entrées du jeu de base dont l'ID est dans mod_ids sont ignorées
      (on ne devrait jamais avoir de conflit, mais par sécurité).
    - Les entrées du mod sont ajoutées à la fin.
    """
    cleaned_base = [e for e in base_list if e.get(id_key) not in mod_ids]
    return cleaned_base + mod_entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    game_dir = Path(sys.argv[1]).expanduser().resolve()

    if not game_dir.is_dir():
        print(f"ERREUR : dossier introuvable → {game_dir}")
        sys.exit(1)

    print(f"\nDossier du jeu détecté : {game_dir}")
    print(f"Dossier du mod         : {MOD_ROOT}\n")

    # ---- Units.json --------------------------------------------------------
    game_units_path = game_dir / UNITS_REL
    mod_units_path  = MOD_ROOT / UNITS_REL

    if not game_units_path.exists():
        print(f"ERREUR : {game_units_path} introuvable.")
        print("Vérifie que le chemin pointe bien vers le dossier racine d'AoH3.")
        sys.exit(1)

    print("Fusion de Units.json …")
    game_units = load_json(game_units_path)
    merged_units = merge(game_units, MOD_UNIT_ENTRIES, "ID", MOD_UNIT_IDS)
    backup(mod_units_path)
    save_json(mod_units_path, merged_units)
    print(f"  → {len(game_units)} entrées du jeu + {len(MOD_UNIT_ENTRIES)} navales = {len(merged_units)} total\n")

    # ---- Technologies.json -------------------------------------------------
    game_tech_path = game_dir / TECHNOLOGIES_REL
    mod_tech_path  = MOD_ROOT / TECHNOLOGIES_REL

    if game_tech_path.exists():
        print("Fusion de Technologies.json …")
        game_techs = load_json(game_tech_path)
        merged_techs = merge(game_techs, MOD_TECH_ENTRIES, "ID", MOD_TECH_IDS)
        backup(mod_tech_path)
        save_json(mod_tech_path, merged_techs)
        print(f"  → {len(game_techs)} techs du jeu + {len(MOD_TECH_ENTRIES)} navales = {len(merged_techs)} total\n")
    else:
        print(f"Technologies.json non trouvé dans le jeu ({game_tech_path}).")
        print("Le fichier du mod (IDs 500-505 uniquement) sera utilisé tel quel.\n")

    print("=" * 60)
    print("Fusion terminée avec succès !")
    print()
    print("Étape suivante :")
    print("  Copie le dossier du mod dans le dossier mods/ du jeu :")
    print(f"    {game_dir}/mods/MaritimeCombatUnits/")
    print("  puis active le mod depuis le menu principal d'AoH3.")
    print("=" * 60)


if __name__ == "__main__":
    main()
