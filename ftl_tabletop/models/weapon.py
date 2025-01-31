class Weapon:
    def __init__(self, name, accuracy_bonus, shots=1, pierce_shields=False, damage=1):
        self.name = name
        self.accuracy_bonus = accuracy_bonus
        self.shots = shots
        self.pierce_shields = pierce_shields
        self.damage = damage

    def __str__(self):
        return f"Weapon({self.name}, +{self.accuracy_bonus}%, {self.shots} shots)"
