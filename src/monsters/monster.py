import time

class Monster(object):
    
    def __init__(self):
        self.level = 0
        self.name = ""
        self.first_spawn_time = 0
        self.respawn_time = 0
        self.hp = 0
        self.current_hp = 0
        self.attackdamage = 0
        self.attackspeed = 0
        self.attackrange = 0
        self.armor = 0
        self.spellblock = 0
        self.gold = 0
        self.exp = 0
        self.range = 0
        self.movespeed = 0


    def fluctuate_status(self, valmin, valmax, level):
        # initial + (max-min)/maxlevel * (level diff)
        return round(valmin + ((valmax-valmin) / 18) * (level - 2))

    def debug(self):
        print("level:" + str(self.level))
        print("armor:" + str(self.armor))
        print("attackdamage:" + str(self.attackdamage))
        print("attackrange:" + str(self.attackrange))
        print("attackspeed:" + str(self.attackspeed))
        print("hp:" + str(self.hp))
        print("current_hp:" + str(self.current_hp))
        print("movespeed:" + str(self.movespeed))
        print("spellblock:" + str(self.spellblock))
        
    def AA(self, target):
        self.aa_start_time = time.time()
        aa_timer = self.aa_start_time - self.aa_end_time
        if aa_timer > 1/self.attackspeed:
            # print("auto attack!")
            target.recieve_damage(float(self.attackdamage), "AD")
            self.aa_end_time = time.time()
        else:
            # print("no auto attack!")
            pass
