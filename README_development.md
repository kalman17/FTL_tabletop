# Directory Structure Suggestion

FTL_tabletop/            # Top-level project folder
├── README.md            # rules for players
├── README_development.md      # development notes
├── requirements.txt     # Python deps (if any) or just note them here
├── main.py              # Entry point for the whole program
├── ftl_tabletop/             # A Python package (folder with __init__.py)
│   ├── __init__.py
│   ├── data/            # Holds JSONs or other resource files
│   │   ├── ships.json
│   │   ├── weapons.json
│   │   └── ...
│   ├── models/          # Classes representing game entities
│   │   ├── ship.py      # Class Ship(...) with stats, etc.
│   │   ├── weapon.py    # Class Weapon(...) with stats, etc.
│   │   └── ...
│   ├── logic/           # Core game logic modules
│   │   ├── attacks.py   # e.g. attack_ship_general, attack_ship_targeted, beams, etc.
│   │   ├── weapons.py   # Functions to handle multi-shot, shield-pierce, etc.
│   │   └── battle_manager.py 
│   ├── gui/             # Tkinter or other GUI code
│   │   ├── battle_gui.py       # All ship-battle-specific GUI
│   │   ├── normal_battle_gui.py # In the future, if you do normal battles
│   │   └── ...
│   ├── states/          # If you want to store game state or session data
│   │   └── game_state.py
│   ├── utils/           # Helpers, e.g. dice rolls, RNG, data loaders
│   │   ├── dice.py
│   │   ├── data_loader.py   # Tools to load JSON ships/weapons
│   │   └── ...
│   └── ...             
└── tests/               # Unit tests (if you add them)
    ├── test_attacks.py
    ├── test_battle_manager.py
    └── ...

# Development Notes

## TODO next
- sometimes there are near misses that still result in hitting the targetted room. ensure it must hit a nearby room
- test if the logic still works well as t_perfect caps at 95, until t_near is 90, after which both go up with a distance of 5
- implement shield points, and shield regen on a turn by turn basis
- count turns
- try creating weapons, ships, and a menu that lets you choose which ship to fight
- choose which weapon to use each turn
- multiplayer (turn by turn against other player on the same machine, coop basically)
- associate systems to rooms, and give levels to systems. keep track of their current status and what effects they have on the ship's battle.

## Weapons
- Weapons can have effects (starting a fire, causing a breach, etc.).
- The chance of these effects occurring depends on the weapon's stats and activates directly if the attack roll is high enough.
- For example, a basic laser has a 10% chance of starting a fire. In code, this means that if you roll a 90 or more, the weapon effect is activated.
- If a weapon can also cause a second effect, e.g., a 10% breach, then you would separate them like this:
  - 80-90 is a breach.
  - 90-100 is a fire.
