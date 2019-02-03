from src.monsters.monster import Monster
import time

class RedBrambleback(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "RedBrambleback"
        self.first_spawn_time = 120 # seconds
        self.respawn_time = 300 # seconds
        self.hp = self.fluctuate_status(2100, 3675, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(82, 303, self.level)
        self.attackspeed = 0.5
        self.armor = self.fluctuate_status(-15, -30, self.level)
        self.spellblock = self.fluctuate_status(10, 20, self.level)
        self.gold = 100
        self.exp = self.fluctuate_status(115, 180, self.level)
        self.range = 100
        self.movespeed = 275
