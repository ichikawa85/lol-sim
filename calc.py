import json
import time

class Champion(object):
    # constractor
    def __init__(self, name):
        f = open("./champions/8.24/" + name + ".json", 'r')
        self.json = json.load(f)
        self.json_data = self.json["data"][name]
        self.name = self.json_data["name"]
        self.armor = self.json_data["stats"]["armor"]
        self.armorperlevel = self.json_data["stats"]["armorperlevel"]
        self.attackdamage = self.json_data["stats"]["attackdamage"]
        self.attackdamageperlevel = self.json_data["stats"]["attackdamageperlevel"]
        self.attackrange = self.json_data["stats"]["attackrange"]
        self.attackspeed = self.json_data["stats"]["attackspeed"]
        self.attackspeedperlevel = self.json_data["stats"]["attackspeedperlevel"] / 100
        self.crit = self.json_data["stats"]["crit"]
        self.critperlevel = self.json_data["stats"]["critperlevel"]
        self.hp = self.json_data["stats"]["hp"]
        self.hpperlevel = self.json_data["stats"]["hpperlevel"]
        self.hpregen = self.json_data["stats"]["hpregen"]
        self.hpregenperlevel = self.json_data["stats"]["hpregenperlevel"]
        self.movespeed = self.json_data["stats"]["movespeed"]
        self.mp = self.json_data["stats"]["mp"]
        self.mpperlevel = self.json_data["stats"]["mpperlevel"]
        self.mpregen = self.json_data["stats"]["mpregen"]
        self.mpregenperlevel = self.json_data["stats"]["mpregenperlevel"]
        self.spellblock = self.json_data["stats"]["spellblock"]
        self.spellblockperlevel = self.json_data["stats"]["spellblockperlevel"]

        self.level = 1
        self.q_level = 0
        self.w_level = 0
        self.e_level = 0
        self.r_level = 0
        self.current_hp = int(self.hp)
        self.current_mp = int(self.mp)
        self.aa_start_time = 0
        self.aa_end_time = 0

    def level_up(self):
        if self.level >= 18:
            return False
        else:
            self.level = self.level + 1
            self.armor = self.armor + self.armorperlevel
            self.attackdamage = self.attackdamage + self.attackdamageperlevel
            self.attackspeed = self.attackspeed + self.attackspeedperlevel
            self.crit = self.crit + self.critperlevel
            self.hp = self.hp + self.hpperlevel
            self.current_hp = self.current_hp + self.hpperlevel
            self.hpregen = self.hpregen + self.hpregenperlevel
            self.mp = self.mp + self.mpperlevel
            self.mpregen = self.mpregen + self.mpregenperlevel
            self.spellblock = self.spellblock + self.spellblockperlevel
            
            return True

    def q_up(self):
        self.q_level += 1
    def w_up(self):
        self.w_level += 1
    def e_up(self):
        self.e_level += 1
    def r_up(self):            
        self.r_level += 1

    def debug_status(self):
        print("armor:" + str(self.armor))
        print("attackdamage:" + str(self.attackdamage))
        print("attackrange:" + str(self.attackrange))
        print("attackspeed:" + str(self.attackspeed))
        print("crit:" + str(self.crit))
        print("hp:" + str(self.hp))
        print("current_hp:" + str(self.current_hp))
        print("hpregen:" + str(self.hpregen))
        print("movespeed:" + str(self.movespeed))
        print("mp:" + str(self.mp))
        print("mpregen:" + str(self.mpregen))
        print("spellblock:" + str(self.spellblock))

        
class Summoner(Champion):
    def __init__(self, name, rune):
        print("name: " + name)
        self.name = name
        self.rune = rune
        super().__init__(self.name)
        self.reflect_rune()
        self.build = []

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

    def recieve_damage(self, prev_damage, type):
        damage = 0
        if "AD" in type:
            damage = prev_damage * 100 / (100 + float(self.armor) )
        if "AP" in type:
            damage = prev_damage * 100 / (100 + float(self.spellblock) )
        self.current_hp = round(self.current_hp - damage)

    def reflect_rune(self):
        # line 1
        if self.rune[0] == 0:
            print('adaptive')
            self.attackdamage = self.json_data["stats"]["attackdamage"]
        elif self.rune[0] == 1:
            self.attackspeed = round(self.attackspeed + 9 / 100, 3)
        elif self.rune[0] == 2:
            print('CDR')
        else:
            raise # parameter error

        # line 2
        if self.rune[1] == 0:
            print('adaptive')
        elif self.rune[1] == 1:
            self.armor = self.armor + 5
        elif self.rune[1] == 2:
            self.spellblock = self.spellblock + 6
        else:
            raise # parameter error

        # line 3
        if self.rune[2] == 0:
            print('adaptive')
        elif self.rune[2] == 1:
            self.armor = self.armor + 5
        elif self.rune[2] == 2:
            self.spellblock = self.spellblock + 6
        else:
            raise # parameter error

    def purchase_item(self, item_id):
        
        

    def debug(self):
        super().debug_status()