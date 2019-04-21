class WeaponComponent:
    def __init__(self, max_range: int = 1, attack_bonus: int = 0, defend_bonus: int = 0, hit_bonus: int = 0,
                 critical_bonus: int = 0, smite: bool = False) -> None:
        self.max_range = max_range
        self.attack_bonus = attack_bonus
        self.defend_bonus = defend_bonus
        self.hit_bonus = hit_bonus
        self.critical_bonus = critical_bonus
        self.smite = smite
