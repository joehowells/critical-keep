class CombatComponent:
    def __init__(self, max_hp, attack_stat, defend_stat, hit_stat, critical_stat):
        self.max_hp = max_hp
        self.cur_hp = max_hp
        self.attack_stat = attack_stat
        self.defend_stat = defend_stat
        self.hit_stat = hit_stat
        self.critical_stat = critical_stat
        self.base_attack_stat = attack_stat
        self.base_defend_stat = defend_stat
        self.base_hit_stat = hit_stat
        self.base_critical_stat = critical_stat
