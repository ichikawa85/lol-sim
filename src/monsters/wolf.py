from src.monsters.monster import Monster
import time

class GreatMarkWolf(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "GreatMarkWolf"
        self.first_spawn_time = 90 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(1300, 2275, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(42, 155, self.level)
        self.attackspeed = 0.625
        self.armor = self.fluctuate_status(10, 20, self.level)
        self.spellblock = 0
        self.gold = 68
        self.exp = self.fluctuate_status(65, 97, self.level)
        self.range = 175
        self.movespeed = 450        
        
class MarkWolf(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "MarkWolf"
        self.first_spawn_time = 90 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(450, 778, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(16, 59, self.level)
        self.attackspeed = 0.625
        self.armor = 0
        self.spellblock = self.fluctuate_status(10, 20, self.level)
        self.gold = 16
        self.exp = self.fluctuate_status(25, 37, self.level)
        self.range = 100
        self.movespeed = 450
