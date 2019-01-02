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
        # my addition
        self.magicdamage = 0
        self.lifesteal = 0
        self.cdr = 0

        # build status
        self.FlatHPPoolMod = 0
        self.FlatMPPoolMod = 0
        self.PercentHPPoolMod = 0
        self.PercentMPPoolMod = 0
        self.FlatHPRegenMod = 0
        self.PercentHPRegenMod = 0
        self.FlatMPRegenMod = 0
        self.PercentMPRegenMod = 0
        self.FlatArmorMod = 0
        self.PercentArmorMod = 0
        self.FlatPhysicalDamageMod = 0
        self.PercentPhysicalDamageMod = 0
        self.FlatMagicDamageMod = 0
        self.PercentMagicDamageMod = 0
        self.FlatMovementSpeedMod = 0
        self.PercentMovementSpeedMod = 0
        self.FlatAttackSpeedMod = 0
        self.PercentAttackSpeedMod = 0
        self.PercentDodgeMod = 0
        self.FlatCritChanceMod = 0
        self.PercentCritChanceMod = 0
        self.FlatCritDamageMod = 0
        self.PercentCritDamageMod = 0
        self.FlatBlockMod = 0
        self.PercentBlockMod = 0
        self.FlatSpellBlockMod = 0
        self.PercentSpellBlockMod = 0
        self.FlatEXPBonus = 0
        self.PercentEXPBonus = 0
        self.FlatEnergyRegenMod = 0
        self.FlatEnergyPoolMod = 0
        self.PercentLifeStealMod = 0
        self.PercentSpellVampMod = 0

        self.level = 1
        self.q_level = 0
        self.w_level = 0
        self.e_level = 0
        self.r_level = 0
        self.current_hp = int(self.hp)
        self.current_mp = int(self.mp)
        self.aa_start_time = 0
        self.aa_end_time = 0

    def level_up(self, count=1):
        if self.level+count > 18:
            return False
        else:
            for i in range(count):
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
        print("level:" + str(self.level))
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
        print("magicdamage:" + str(self.magicdamage))
        print("lifesteal:" + str(self.lifesteal))
        print("cdr:" + str(self.cdr))

        
class Summoner(Champion):
    def __init__(self, name, rune):
        print("name: " + name)
        self.name = name
        self.rune = rune
        super().__init__(self.name)
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
            if self.FlatPhysicalDamageMod >= self.FlatMagicDamageMod:
                self.attackdamage = self.attackdamage + 6
            else:
                self.magicdamage = self.magicdamage + 10
        elif self.rune[0] == 1:
            self.attackspeed = round(self.attackspeed + 9 / 100, 3)
        elif self.rune[0] == 2:
            self.cdr = round(self.cdr + 10 * self.level / 18)
        else:
            raise # parameter error

        # line 2
        if self.rune[1] == 0:
            if self.FlatPhysicalDamageMod >= self.FlatMagicDamageMod:
                self.attackdamage = self.attackdamage + 6
            else:
                self.magicdamage = self.magicdamage + 10
        elif self.rune[1] == 1:
            self.armor = self.armor + 5
        elif self.rune[1] == 2:
            self.spellblock = self.spellblock + 6
        else:
            raise # parameter error

        # line 3
        if self.rune[2] == 0:
            rune_bonus = round(15 + (75 / 18) * (self.level - 1 )) # initial + (max-min)/maxlevel * (level diff)
            self.hp = self.hp + rune_bonus
        elif self.rune[2] == 1:
            self.armor = self.armor + 5
        elif self.rune[2] == 2:
            self.spellblock = self.spellblock + 6
        else:
            raise # parameter error

    def reflect_build(self, item_id):
        f = open("./item/8.24.1/item.json", 'r')        
        self.json = json.load(f)
        self.json_data = self.json["data"]
        self.item = self.json_data[str(item_id)]
        print(self.item["stats"])
        # print(self.item["effect"]) # => TBD
        for i in self.item["stats"]:
            if 'FlatArmorMod' in i:
                self.FlatArmorMod = self.FlatArmorMod + self.item["stats"][i]
                self.armor = self.armor + self.item["stats"][i]
            elif 'FlatPhysicalDamageMod' in i:
                self.FlatPhysicalDamageMod = self.FlatPhysicalDamageMod + self.item["stats"][i]
                self.attackdamage = self.attackdamage + self.item["stats"][i]
            elif 'PercentAttackSpeedMod' in i:
                self.PercentAttackSpeedMod = self.PercentAttackSpeedMod + self.item["stats"][i]
                self.attackspeed = self.attackspeed + self.item["stats"][i] / 100
            elif 'FlatCritChanceMod' in i:
                self.FlatCritChanceMod = self.FlatCritChanceMod + self.item["stats"][i]
                self.crit = self.crit + self.item["stats"][i]
            elif 'FlatHPPoolMod' in i:
                self.FlatHPPoolMod = self.FlatHPPoolMod + self.item["stats"][i]
                self.hp = self.hp + self.item["stats"][i]
            elif 'FlatHPRegenMod' in i:
                self.FlatHPRegenMod = self.FlatHPRegenMod + self.item["stats"][i]
                self.hpregen = self.hpregen + self.item["stats"][i]
            elif 'FlatMPPoolMod' in i:
                self.FlatMPPoolMod = self.FlatMPPoolMod + self.item["stats"][i]
                self.mp = self.mp + self.item["stats"][i]
            elif 'FlatMPRegenMod' in i:
                self.FlatMPRegenMod = self.FlatMPRegenMod + self.item["stats"][i]
                self.mpregen = self.mpregen + self.item["stats"][i]
            elif 'FlatMovementSpeedMod' in i:
                self.FlatMovementSpeedMod = self.FlatMovementSpeedMod + self.item["stats"][i]
                self.movespeed = self.movespeed + self.item["stats"][i] 
            elif 'PercentMovementSpeedMod' in i:
                self.PercentMovementSpeedMod = self.PercentMovementSpeedMod + self.item["stats"][i]
                self.movespeed = self.movespeed * (1 + self.item["stats"][i])
            elif 'FlatSpellBlockMod' in i:
                self.FlatSpellBlockMod = self.FlatSpellBlockMod + self.item["stats"][i]
                self.spellblock = self.spellblock + self.item["stats"][i]
            elif 'FlatMagicDamageMod' in i:
                self.FlatMagicDamageMod = self.FlatMagicDamageMod + self.item["stats"][i]                
                self.magicdamage = self.magicdamage + self.item["stats"][i]
            elif 'PercentLifeStealMod' in i:
                self.PercentLifeStealMod = self.PercentLifeStealMod + self.item["stats"][i]                
                self.lifesteal = self.lifesteal + self.item["stats"][i]

        
    def purchase_item(self, item_id):
        self.build.append(item_id)
        self.reflect_build(item_id)

        
    def sell_item(self, item_id):
        if item_id in self.build:
            self.build.remove(item_id)
        else:
            pass
        self.reflect_build(item_id)

    def debug(self):
        super().debug_status()
