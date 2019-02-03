from src.monsters.monster import Monster
import time

class RiftScuttler(Monster):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.name = "RiftScuttler"
        self.first_spawn_time = 120 # seconds
        self.respawn_time = 150 # seconds
        self.hp = self.fluctuate_status(1200, 2480, self.level)
        self.current_hp = self.hp
        self.attackdamage = self.fluctuate_status(35, 116, self.level)
        self.attackspeed = 0.638
        self.armor = 60
        self.spellblock = 60
        self.gold = self.fluctuate_status(70, 140, self.level)
        self.exp = self.fluctuate_status(115, 230, self.level)
        self.range = 0
        self.movespeed = 155
        
