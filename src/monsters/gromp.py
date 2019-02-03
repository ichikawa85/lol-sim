from src.monsters.monster import Monster
import time

class Gromp(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "gromp"
        self.first_spawn_time = 102 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(1800, 3150, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(70, 259, self.level)
        self.attackspeed = 1.004
        self.armor = 0
        self.spellblock = self.fluctuate_status(-15, -30, self.level)
        self.gold = 86
        self.exp = self.fluctuate_status(115, 172, self.level)
        self.range = 250
        self.movespeed = 330
        
