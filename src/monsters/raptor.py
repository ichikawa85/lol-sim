from src.monsters.monster import Monster
import time

class CrimsonRaptor(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "CrimsonRaptor"
        self.first_spawn_time = 90 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(700, 1225, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(20, 74, self.level)
        self.attackspeed = 0.667
        self.armor = self.fluctuate_status(30, 60, self.level)
        self.spellblock = self.fluctuate_status(30, 60, self.level)
        self.gold = 62
        self.exp = self.fluctuate_status(20, 30, self.level)
        self.range = 300
        self.movespeed = 350        
        
class Raptor(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "Raptor"
        self.first_spawn_time = 90 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(400, 680, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(13, 56, self.level)
        self.attackspeed = 1.0
        self.armor = 0
        self.spellblock = 0
        self.gold = 10
        self.exp = self.fluctuate_status(20, 30, self.level)
        self.range = 100
        self.movespeed = 450
        
