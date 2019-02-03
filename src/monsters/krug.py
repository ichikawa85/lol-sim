from src.monsters.monster import Monster
import time

class AncientKrug(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "AncientKrug"
        self.first_spawn_time = 102 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(1250, 2188, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(80, 296, self.level)
        self.attackspeed = 0.613
        self.armor = self.fluctuate_status(10, 20, self.level)
        self.spellblock = self.fluctuate_status(-15, -30, self.level)
        self.gold = 70
        self.exp = self.fluctuate_status(70, 150, self.level)
        self.range = 150
        self.movespeed = 185
        
class Krug(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "Krug"
        self.first_spawn_time = 102 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(500, 875, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(25, 93, self.level)
        self.attackspeed = 0.613
        self.armor = 0
        self.spellblock = 0
        self.gold = 10
        self.exp = self.fluctuate_status(35, 52, self.level)
        self.range = 110
        self.movespeed = 285

class MiniKrug(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "MiniKrug"
        self.first_spawn_time = 102 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(60, 105, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(17, 60, self.level)
        self.attackspeed = 0.613
        self.armor = 0
        self.spellblock = 0
        self.gold = 10
        self.exp = self.fluctuate_status(7, 10, self.level)
        self.range = 110
        self.movespeed = 335
