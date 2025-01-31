class Ship:
    def __init__(self, name, evasion, hull, rooms, shield=0, weapons=None):
        self.name = name
        self.evasion = evasion
        self.hull = hull
        self.rooms = rooms
        self.shield = shield
        self.weapons = weapons or []

    def is_destroyed(self):
        return self.hull <= 0
