# Maritime Combat Units — Age of History III Mod

Adds **5 new naval unit types** (15 units total with upgrade tiers) to Age of History III, covering the full arc of maritime warfare from the Age of Sail to the modern era.

---

## New Units

| Type | ID | Tiers | Era |
|---|---|---|---|
| **Frigate** | 100 | Frigate → Heavy Frigate → Frigate Squadron | Age of Sail |
| **Ship of the Line** | 101 | Ship of the Line → 2nd Rate Ship → 1st Rate Ship | Age of Sail |
| **Ironclad** | 102 | Ironclad → Advanced Ironclad → Ironclad Dreadnought | Industrial |
| **Battleship** | 103 | Battleship → Dreadnought → Super Battleship | Modern |
| **Destroyer** | 104 | Torpedo Boat → Destroyer → Fleet Destroyer | Industrial–Modern |

### Stats overview

| Unit | Attack | Defense | Speed | Range | Cost | Maintenance |
|---|---|---|---|---|---|---|
| Frigate | 8 | 5 | 2.8 | 2 | 80 | 1.2 |
| Heavy Frigate | 14 | 10 | 2.8 | 2 | 140 | 2.0 |
| Frigate Squadron | 22 | 16 | 3.0 | 3 | 220 | 3.2 |
| Ship of the Line | 22 | 18 | 2.0 | 3 | 220 | 3.5 |
| 2nd Rate Ship | 32 | 27 | 2.0 | 3 | 340 | 5.0 |
| 1st Rate Ship | 45 | 38 | 2.2 | 4 | 480 | 7.0 |
| Ironclad | 42 | 50 | 2.2 | 3 | 420 | 6.5 |
| Advanced Ironclad | 58 | 68 | 2.4 | 3 | 580 | 9.0 |
| Ironclad Dreadnought | 78 | 90 | 2.6 | 4 | 780 | 12.0 |
| Battleship | 85 | 78 | 2.6 | 5 | 900 | 14.0 |
| Dreadnought | 115 | 105 | 2.8 | 5 | 1200 | 19.0 |
| Super Battleship | 150 | 135 | 3.0 | 6 | 1600 | 25.0 |
| **Torpedo Boat** | **30** | **12** | **3.2** | **2** | **280** | **4.5** |
| **Destroyer** | **55** | **35** | **3.2** | **3** | **550** | **9.0** |
| **Fleet Destroyer** | **95** | **70** | **3.4** | **4** | **950** | **15.0** |

### Destroyer unit role

The **Destroyer line** fills a fast-raider/fleet-escort niche distinct from the heavy capital ship lines:

- **High speed** (3.2–3.4) — the fastest naval units in the mod
- **Strong attack relative to cost** — ideal for harassing slower capital ships
- **Lower defense** — vulnerable to concentrated fire from battleships
- **Dedicated tech branch** (IDs 510–512) branching from Naval Warfare (500)

---

## Technology Tree

### Capital ship branch (Row 3, columns 20–25)

| ID | Name | Cost | Unlocks | Requires |
|---|---|---|---|---|
| 500 | Naval Warfare | 150 | Ironclad | — |
| 501 | Steam Propulsion | 280 | Advanced Ironclad | 500 |
| 502 | Iron Hulls | 450 | Ironclad Dreadnought | 501 |
| 503 | Steel Naval Engineering | 650 | Battleship | 502 |
| 504 | Modern Naval Gunnery | 900 | Dreadnought | 503 |
| 505 | Naval Supremacy | 1300 | Super Battleship | 504 |

### Destroyer branch (Row 4, columns 21–23)

| ID | Name | Cost | Unlocks | Requires |
|---|---|---|---|---|
| 510 | Torpedo Warfare | 250 | Torpedo Boat | 500 |
| 511 | Destroyer Design | 420 | Destroyer | 510 |
| 512 | Guided Missile Systems | 750 | Fleet Destroyer | 511 |

---

## Installation

### Manual install
1. Copy the entire mod folder into your game's `mods/` directory:
   ```
   <AoH3 install>/mods/MaritimeCombatUnits/
   ```
2. The folder structure inside the mod must be:
   ```
   MaritimeCombatUnits/
   └── game/
       ├── languages/
       │   ├── EN.properties
       │   └── FR.properties
       ├── technologies/
       │   └── Technologies.json
       └── units/
           ├── Units.json
           ├── Frigate.json
           ├── ShipOfTheLine.json
           ├── Ironclad.json
           ├── Battleship.json
           ├── Destroyer.json
           └── unitsImages/
               ├── H/      (16×16 PNGs)
               ├── XH/     (32×32 PNGs)
               └── XXH/    (48×48 PNGs)
   ```
3. **Merge `Units.json` and `Technologies.json`**: these files normally replace the base-game files.
   Open the base game's versions, copy their entries, then append the new entries from this mod at the end.
   Make sure each entry keeps a unique `ID`.

### Generating unit images
Placeholder PNG images (solid-colour ship silhouettes) are pre-generated in `game/units/unitsImages/`.
To regenerate them (e.g. after editing `generate_unit_images.py` to use custom art):
```bash
python3 generate_unit_images.py
```
Requires Python 3.10+ (no third-party dependencies).

---

## File Reference

| File | Purpose |
|---|---|
| `game/units/Units.json` | Registers the 5 new unit types in the game |
| `game/units/Frigate.json` | Frigate upgrade tree (3 levels) |
| `game/units/ShipOfTheLine.json` | Ship of the Line upgrade tree (3 levels) |
| `game/units/Ironclad.json` | Ironclad upgrade tree (3 levels) |
| `game/units/Battleship.json` | Battleship upgrade tree (3 levels) |
| `game/units/Destroyer.json` | Destroyer upgrade tree (3 levels) |
| `game/technologies/Technologies.json` | Naval technology tree (IDs 500–505, 510–512) |
| `game/languages/EN.properties` | English names & descriptions |
| `game/languages/FR.properties` | French names & descriptions |
| `generate_unit_images.py` | Script to regenerate placeholder PNGs |

---

## Customisation

- **Tech requirements**: edit `RequiredTechID` in each unit JSON to match your scenario's tech tree.
- **Balance**: all stats (`Attack`, `Defense`, `Cost`, etc.) are plain numbers — edit freely.
- **Custom artwork**: replace the PNG files in `unitsImages/H`, `XH`, `XXH` with your own designs at the matching `ImageID` filename (e.g. `140.png` for the basic Torpedo Boat).
- **More languages**: copy `EN.properties`, translate, and rename to your language code (e.g. `DE.properties`).

---

## Compatibility

- Age of History III (all versions as of 2024–2025)
- Does **not** overwrite any existing unit — safe to combine with other mods that don't use:
  - Unit IDs **100–104**
  - Image IDs **100–102**, **110–112**, **120–122**, **130–132**, **140–142**
  - Technology IDs **500–505**, **510–512**
