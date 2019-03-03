import json
import time
import copy

class Champion(object):
    # constractor
    def __init__(self, name, version):
        f = open("./champions/" + version + "/" + name + ".json", 'r')
        f_item = open("./item/" + version + "/item.json", 'r')
        self.json = json.load(f)
        self.json_data = self.json["data"][name]
        self.json_item = json.load(f_item)
        self.json_item_data = self.json_item["data"]
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

        self.rune_bonus = {}

        # for UNDO
        self.pre_armor = self.json_data["stats"]["armor"]
        self.pre_armorperlevel = self.json_data["stats"]["armorperlevel"]
        self.pre_attackdamage = self.json_data["stats"]["attackdamage"]
        self.pre_attackdamageperlevel = self.json_data["stats"]["attackdamageperlevel"]
        self.pre_attackrange = self.json_data["stats"]["attackrange"]
        self.pre_attackspeed = self.json_data["stats"]["attackspeed"]
        self.pre_attackspeedperlevel = self.json_data["stats"]["attackspeedperlevel"] / 100
        self.pre_crit = self.json_data["stats"]["crit"]
        self.pre_critperlevel = self.json_data["stats"]["critperlevel"]
        self.pre_hp = self.json_data["stats"]["hp"]
        self.pre_hpperlevel = self.json_data["stats"]["hpperlevel"]
        self.pre_hpregen = self.json_data["stats"]["hpregen"]
        self.pre_hpregenperlevel = self.json_data["stats"]["hpregenperlevel"]
        self.pre_movespeed = self.json_data["stats"]["movespeed"]
        self.pre_mp = self.json_data["stats"]["mp"]
        self.pre_mpperlevel = self.json_data["stats"]["mpperlevel"]
        self.pre_mpregen = self.json_data["stats"]["mpregen"]
        self.pre_mpregenperlevel = self.json_data["stats"]["mpregenperlevel"]
        self.pre_spellblock = self.json_data["stats"]["spellblock"]
        self.pre_spellblockperlevel = self.json_data["stats"]["spellblockperlevel"]
        self.pre_magicdamage = 0
        self.pre_lifesteal = 0
        self.pre_pre_cdr = 0
        self.pre_FlatHPPoolMod = 0
        self.pre_FlatMPPoolMod = 0
        self.pre_PercentHPPoolMod = 0
        self.pre_PercentMPPoolMod = 0
        self.pre_FlatHPRegenMod = 0
        self.pre_PercentHPRegenMod = 0
        self.pre_FlatMPRegenMod = 0
        self.pre_PercentMPRegenMod = 0
        self.pre_FlatArmorMod = 0
        self.pre_PercentArmorMod = 0
        self.pre_FlatPhysicalDamageMod = 0
        self.pre_PercentPhysicalDamageMod = 0
        self.pre_FlatMagicDamageMod = 0
        self.pre_PercentMagicDamageMod = 0
        self.pre_FlatMovementSpeedMod = 0
        self.pre_PercentMovementSpeedMod = 0
        self.pre_FlatAttackSpeedMod = 0
        self.pre_PercentAttackSpeedMod = 0
        self.pre_PercentDodgeMod = 0
        self.pre_FlatCritChanceMod = 0
        self.pre_PercentCritChanceMod = 0
        self.pre_FlatCritDamageMod = 0
        self.pre_PercentCritDamageMod = 0
        self.pre_FlatBlockMod = 0
        self.pre_PercentBlockMod = 0
        self.pre_FlatSpellBlockMod = 0
        self.pre_PercentSpellBlockMod = 0
        self.pre_FlatEXPBonus = 0
        self.pre_PercentEXPBonus = 0
        self.pre_FlatEnergyRegenMod = 0
        self.pre_FlatEnergyPoolMod = 0
        self.pre_PercentLifeStealMod = 0
        self.pre_PercentSpellVampMod = 0

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

    def level_up_to(self, destination):
        if destination > 18:
            print("Error: Level is overflow!")
            return False
        else:
            count = destination - self.level
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

    def backup_status(self):
        self.pre_armor	= self.armor
        self.pre_armorperlevel	= self.armorperlevel
        self.pre_attackdamage	= self.attackdamage
        self.pre_attackdamageperlevel	= self.attackdamageperlevel
        self.pre_attackrange	= self.attackrange
        self.pre_attackspeed	= self.attackspeed
        self.pre_attackspeedperlevel	= self.attackspeedperlevel
        self.pre_crit	= self.crit
        self.pre_critperlevel	= self.critperlevel
        self.pre_hp	= self.hp
        self.pre_hpperlevel	= self.hpperlevel
        self.pre_hpregen	= self.hpregen
        self.pre_hpregenperlevel	= self.hpregenperlevel
        self.pre_movespeed	= self.movespeed
        self.pre_mp	= self.mp
        self.pre_mpperlevel	= self.mpperlevel
        self.pre_mpregen	= self.mpregen
        self.pre_mpregenperlevel	= self.mpregenperlevel
        self.pre_spellblock	= self.spellblock
        self.pre_spellblockperlevel	= self.spellblockperlevel
        self.pre_magicdamage	= self.magicdamage
        self.pre_lifesteal	= self.lifesteal
        self.pre_cdr	= self.cdr
        self.pre_FlatHPPoolMod	= self.FlatHPPoolMod
        self.pre_FlatMPPoolMod	= self.FlatMPPoolMod
        self.pre_PercentHPPoolMod	= self.PercentHPPoolMod
        self.pre_PercentMPPoolMod	= self.PercentMPPoolMod
        self.pre_FlatHPRegenMod	= self.FlatHPRegenMod
        self.pre_PercentHPRegenMod	= self.PercentHPRegenMod
        self.pre_FlatMPRegenMod	= self.FlatMPRegenMod
        self.pre_PercentMPRegenMod	= self.PercentMPRegenMod
        self.pre_FlatArmorMod	= self.FlatArmorMod
        self.pre_PercentArmorMod	= self.PercentArmorMod
        self.pre_FlatPhysicalDamageMod	= self.FlatPhysicalDamageMod
        self.pre_PercentPhysicalDamageMod	= self.PercentPhysicalDamageMod
        self.pre_FlatMagicDamageMod	= self.FlatMagicDamageMod
        self.pre_PercentMagicDamageMod	= self.PercentMagicDamageMod
        self.pre_FlatMovementSpeedMod	= self.FlatMovementSpeedMod
        self.pre_PercentMovementSpeedMod	= self.PercentMovementSpeedMod
        self.pre_FlatAttackSpeedMod	= self.FlatAttackSpeedMod
        self.pre_PercentAttackSpeedMod	= self.PercentAttackSpeedMod
        self.pre_PercentDodgeMod	= self.PercentDodgeMod
        self.pre_FlatCritChanceMod	= self.FlatCritChanceMod
        self.pre_PercentCritChanceMod	= self.PercentCritChanceMod
        self.pre_FlatCritDamageMod	= self.FlatCritDamageMod
        self.pre_PercentCritDamageMod	= self.PercentCritDamageMod
        self.pre_FlatBlockMod	= self.FlatBlockMod
        self.pre_PercentBlockMod	= self.PercentBlockMod
        self.pre_FlatSpellBlockMod	= self.FlatSpellBlockMod
        self.pre_PercentSpellBlockMod	= self.PercentSpellBlockMod
        self.pre_FlatEXPBonus	= self.FlatEXPBonus
        self.pre_PercentEXPBonus	= self.PercentEXPBonus
        self.pre_FlatEnergyRegenMod	= self.FlatEnergyRegenMod
        self.pre_FlatEnergyPoolMod	= self.FlatEnergyPoolMod
        self.pre_PercentLifeStealMod	= self.PercentLifeStealMod
        self.pre_PercentSpellVampMod	= self.PercentSpellVampMod

    def rollback_status(self):
        self.armor	= self.pre_armor
        self.armorperlevel	= self.pre_armorperlevel
        self.attackdamage	= self.pre_attackdamage
        self.attackdamageperlevel	= self.pre_attackdamageperlevel
        self.attackrange	= self.pre_attackrange
        self.attackspeed	= self.pre_attackspeed
        self.attackspeedperlevel	= self.pre_attackspeedperlevel
        self.crit	= self.pre_crit
        self.critperlevel	= self.pre_critperlevel
        self.hp	= self.pre_hp
        self.hpperlevel	= self.pre_hpperlevel
        self.hpregen	= self.pre_hpregen
        self.hpregenperlevel	= self.pre_hpregenperlevel
        self.movespeed	= self.pre_movespeed
        self.mp	= self.pre_mp
        self.mpperlevel	= self.pre_mpperlevel
        self.mpregen	= self.pre_mpregen
        self.mpregenperlevel	= self.pre_mpregenperlevel
        self.spellblock	= self.pre_spellblock
        self.spellblockperlevel	= self.pre_spellblockperlevel
        self.magicdamage	= self.pre_magicdamage
        self.lifesteal	= self.pre_lifesteal
        self.cdr	= self.pre_cdr
        self.FlatHPPoolMod	= self.pre_FlatHPPoolMod
        self.FlatMPPoolMod	= self.pre_FlatMPPoolMod
        self.PercentHPPoolMod	= self.pre_PercentHPPoolMod
        self.PercentMPPoolMod	= self.pre_PercentMPPoolMod
        self.FlatHPRegenMod	= self.pre_FlatHPRegenMod
        self.PercentHPRegenMod	= self.pre_PercentHPRegenMod
        self.FlatMPRegenMod	= self.pre_FlatMPRegenMod
        self.PercentMPRegenMod	= self.pre_PercentMPRegenMod
        self.FlatArmorMod	= self.pre_FlatArmorMod
        self.PercentArmorMod	= self.pre_PercentArmorMod
        self.FlatPhysicalDamageMod	= self.pre_FlatPhysicalDamageMod
        self.PercentPhysicalDamageMod	= self.pre_PercentPhysicalDamageMod
        self.FlatMagicDamageMod	= self.pre_FlatMagicDamageMod
        self.PercentMagicDamageMod	= self.pre_PercentMagicDamageMod
        self.FlatMovementSpeedMod	= self.pre_FlatMovementSpeedMod
        self.PercentMovementSpeedMod	= self.pre_PercentMovementSpeedMod
        self.FlatAttackSpeedMod	= self.pre_FlatAttackSpeedMod
        self.PercentAttackSpeedMod	= self.pre_PercentAttackSpeedMod
        self.PercentDodgeMod	= self.pre_PercentDodgeMod
        self.FlatCritChanceMod	= self.pre_FlatCritChanceMod
        self.PercentCritChanceMod	= self.pre_PercentCritChanceMod
        self.FlatCritDamageMod	= self.pre_FlatCritDamageMod
        self.PercentCritDamageMod	= self.pre_PercentCritDamageMod
        self.FlatBlockMod	= self.pre_FlatBlockMod
        self.PercentBlockMod	= self.pre_PercentBlockMod
        self.FlatSpellBlockMod	= self.pre_FlatSpellBlockMod
        self.PercentSpellBlockMod	= self.pre_PercentSpellBlockMod
        self.FlatEXPBonus	= self.pre_FlatEXPBonus
        self.PercentEXPBonus	= self.pre_PercentEXPBonus
        self.FlatEnergyRegenMod	= self.pre_FlatEnergyRegenMod
        self.FlatEnergyPoolMod	= self.pre_FlatEnergyPoolMod
        self.PercentLifeStealMod	= self.pre_PercentLifeStealMod
        self.PercentSpellVampMod	= self.pre_PercentSpellVampMod        

    def debug_status(self, param=None):
        if param is None:
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
        else:
            exe_str = "self." + param
            print(param+":"+str(eval(exe_str)))

    def debug_skill_level(self):
        print("Q:" + str(self.q_level))
        print("W:" + str(self.w_level))
        print("E:" + str(self.e_level))
        print("R:" + str(self.r_level))        

RUNE_BONUS_AD = 5.4
RUNE_BONUS_AP = 9
RUNE_BONUS_AS = 10
RUNE_BONUS_AR = 6
RUNE_BONUS_MR = 8
         
class Summoner(Champion):
    def __init__(self, name, rune, version):
        print("name: " + name)
        self.name = name
        self.rune = rune
        super().__init__(self.name, version)
        self.build = []
        self.pre_build = []

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
        self.rune_bonus = []
        self.rune_bonus_first = {}
        self.rune_bonus_second = {}
        self.rune_bonus_third = {}
        
        # line 1
        if self.rune[0] == 0:
            if self.FlatPhysicalDamageMod >= self.FlatMagicDamageMod:
                self.attackdamage = self.attackdamage + RUNE_BONUS_AD
                self.rune_bonus_first["AD"] = RUNE_BONUS_AD
            else:
                self.magicdamage = self.magicdamage + RUNE_BONUS_AP
                self.rune_bonus_first["AP"] = RUNE_BONUS_AP
        elif self.rune[0] == 1:
            self.attackspeed = round(self.attackspeed + RUNE_BONUS_AS / 100, 3)
            self.rune_bonus_first["AS"] = RUNE_BONUS_AS / 100
        elif self.rune[0] == 2:
            self.cdr = round(self.cdr + 10 * self.level / 18)
            self.rune_bonus_first["CDR"] = 10 * self.level / 18
        else:
            raise # parameter error
        self.rune_bonus.append(self.rune_bonus_first)

        # line 2
        if self.rune[1] == 0:
            if self.FlatPhysicalDamageMod >= self.FlatMagicDamageMod:
                self.attackdamage = self.attackdamage + RUNE_BONUS_AD
                self.rune_bonus_second["AD"] = RUNE_BONUS_AD
            else:
                self.magicdamage = self.magicdamage + RUNE_BONUS_AP
                self.rune_bonus_second["AP"] = RUNE_BONUS_AP
        elif self.rune[1] == 1:
            self.armor = self.armor + RUNE_BONUS_AR
            self.rune_bonus_second["AR"] = RUNE_BONUS_AR
        elif self.rune[1] == 2:
            self.spellblock = self.spellblock + RUNE_BONUS_MR
            self.rune_bonus_second["MR"] = RUNE_BONUS_MR
        else:
            raise # parameter error
        self.rune_bonus.append(self.rune_bonus_second)

        # line 3
        if self.rune[2] == 0:
            rune_bonus_hp = round(15 + (75 / 18) * (self.level - 1 )) # initial + (max-min)/maxlevel * (level diff)
            self.hp = self.hp + rune_bonus_hp
            self.rune_bonus_third["HP"] = rune_bonus_hp
        elif self.rune[2] == 1:
            self.armor = self.armor + RUNE_BONUS_AR
            self.rune_bonus_third["AR"] = RUNE_BONUS_AR
        elif self.rune[2] == 2:
            self.spellblock = self.spellblock + RUNE_BONUS_MR
            self.rune_bonus_third["MR"] = RUNE_BONUS_MR
        else:
            raise # parameter error
        
        self.rune_bonus.append(self.rune_bonus_third)

    def refresh_rune(self):
        for bonus in self.rune_bonus:
            if 'AD' in bonus:
                self.attackdamage = self.attackdamage - bonus["AD"]
            elif 'AP' in bonus:
                self.magicdamage = self.magicdamage - bonus["AP"]
            elif 'CDR' in bonus:
                self.cdr = self.cdr - bonus["CDR"]
            elif 'HP' in bonus:
                self.hp = self.hp - bonus["HP"]
            elif 'AR' in bonus:
                self.armor = self.armor - bonus["AR"]
            elif 'MR' in bonus:
                self.spellblock = self.spellblock - bonus["MR"]

        self.reflect_rune()

    def reflect_build(self, item_id, sell_flag):
        item = self.json_item_data[str(item_id)]
        # print(item["stats"])
        # print(item["effect"]) # => TBD
        # ステラックの籠手の場合は特別にpassiveを追加
        if item_id == 3053:
            base_ad = self.attackdamage - self.FlatPhysicalDamageMod
            print("base_ad: " + str(base_ad))
            self.FlatPhysicalDamageMod = self.FlatPhysicalDamageMod + base_ad / 2
            self.attackdamage = self.attackdamage + base_ad / 2
        
        for i in item["stats"]:
            if sell_flag is False:
                if 'FlatArmorMod' in i:
                    self.FlatArmorMod = self.FlatArmorMod + item["stats"][i]
                    self.armor = self.armor + item["stats"][i]
                elif 'FlatPhysicalDamageMod' in i:
                    self.FlatPhysicalDamageMod = self.FlatPhysicalDamageMod + item["stats"][i]
                    self.attackdamage = self.attackdamage + item["stats"][i]
                elif 'PercentAttackSpeedMod' in i:
                    self.PercentAttackSpeedMod = self.PercentAttackSpeedMod + item["stats"][i]
                    self.attackspeed = self.attackspeed + item["stats"][i] / 100
                elif 'FlatCritChanceMod' in i:
                    self.FlatCritChanceMod = self.FlatCritChanceMod + item["stats"][i]
                    self.crit = self.crit + item["stats"][i]
                elif 'FlatHPPoolMod' in i:
                    self.FlatHPPoolMod = self.FlatHPPoolMod + item["stats"][i]
                    self.hp = self.hp + item["stats"][i]
                elif 'FlatHPRegenMod' in i:
                    self.FlatHPRegenMod = self.FlatHPRegenMod + item["stats"][i]
                    self.hpregen = self.hpregen + item["stats"][i]
                elif 'FlatMPPoolMod' in i:
                    self.FlatMPPoolMod = self.FlatMPPoolMod + item["stats"][i]
                    self.mp = self.mp + item["stats"][i]
                elif 'FlatMPRegenMod' in i:
                    self.FlatMPRegenMod = self.FlatMPRegenMod + item["stats"][i]
                    self.mpregen = self.mpregen + item["stats"][i]
                elif 'FlatMovementSpeedMod' in i:
                    self.FlatMovementSpeedMod = self.FlatMovementSpeedMod + item["stats"][i]
                    self.movespeed = self.movespeed + item["stats"][i] 
                elif 'PercentMovementSpeedMod' in i:
                    self.PercentMovementSpeedMod = self.PercentMovementSpeedMod + item["stats"][i]
                    self.movespeed = self.movespeed * (1 + item["stats"][i])
                elif 'FlatSpellBlockMod' in i:
                    self.FlatSpellBlockMod = self.FlatSpellBlockMod + item["stats"][i]
                    self.spellblock = self.spellblock + item["stats"][i]
                elif 'FlatMagicDamageMod' in i:
                    self.FlatMagicDamageMod = self.FlatMagicDamageMod + item["stats"][i]                
                    self.magicdamage = self.magicdamage + item["stats"][i]
                elif 'PercentLifeStealMod' in i:
                    self.PercentLifeStealMod = self.PercentLifeStealMod + item["stats"][i]                
                    self.lifesteal = self.lifesteal + item["stats"][i]
            elif sell_flag is True:
                if 'FlatArmorMod' in i:
                    self.FlatArmorMod = self.FlatArmorMod - item["stats"][i]
                    self.armor = self.armor - item["stats"][i]
                elif 'FlatPhysicalDamageMod' in i:
                    self.FlatPhysicalDamageMod = self.FlatPhysicalDamageMod - item["stats"][i]
                    self.attackdamage = self.attackdamage - item["stats"][i]
                elif 'PercentAttackSpeedMod' in i:
                    self.PercentAttackSpeedMod = self.PercentAttackSpeedMod - item["stats"][i]
                    self.attackspeed = self.attackspeed - item["stats"][i] / 100
                elif 'FlatCritChanceMod' in i:
                    self.FlatCritChanceMod = self.FlatCritChanceMod - item["stats"][i]
                    self.crit = self.crit - item["stats"][i]
                elif 'FlatHPPoolMod' in i:
                    self.FlatHPPoolMod = self.FlatHPPoolMod - item["stats"][i]
                    self.hp = self.hp - item["stats"][i]
                elif 'FlatHPRegenMod' in i:
                    self.FlatHPRegenMod = self.FlatHPRegenMod - item["stats"][i]
                    self.hpregen = self.hpregen - item["stats"][i]
                elif 'FlatMPPoolMod' in i:
                    self.FlatMPPoolMod = self.FlatMPPoolMod - item["stats"][i]
                    self.mp = self.mp - item["stats"][i]
                elif 'FlatMPRegenMod' in i:
                    self.FlatMPRegenMod = self.FlatMPRegenMod - item["stats"][i]
                    self.mpregen = self.mpregen - item["stats"][i]
                elif 'FlatMovementSpeedMod' in i:
                    self.FlatMovementSpeedMod = self.FlatMovementSpeedMod - item["stats"][i]
                    self.movespeed = self.movespeed - item["stats"][i] 
                elif 'PercentMovementSpeedMod' in i:
                    self.PercentMovementSpeedMod = self.PercentMovementSpeedMod - item["stats"][i]
                    self.movespeed = self.movespeed * (1 - item["stats"][i])
                elif 'FlatSpellBlockMod' in i:
                    self.FlatSpellBlockMod = self.FlatSpellBlockMod - item["stats"][i]
                    self.spellblock = self.spellblock - item["stats"][i]
                elif 'FlatMagicDamageMod' in i:
                    self.FlatMagicDamageMod = self.FlatMagicDamageMod - item["stats"][i]                
                    self.magicdamage = self.magicdamage - item["stats"][i]
                elif 'PercentLifeStealMod' in i:
                    self.PercentLifeStealMod = self.PercentLifeStealMod - item["stats"][i]                
                    self.lifesteal = self.lifesteal - item["stats"][i]


    def purchase_item(self, item_id):
        if item_id != 0:
            self.pre_build = copy.copy(self.build)
            self.build.append(item_id)
            self.backup_status()
            self.reflect_build(item_id, False)
        else:
            pass
        
    def sell_item(self, item_id):
        if item_id != 0:
            if item_id in self.build:
                self.pre_build = copy.copy(self.build)
                self.build.remove(item_id)
            else:
                pass
            self.backup_status()
            self.reflect_build(item_id, True)
        else:
            pass

    def undo_item(self):
        self.build = copy.copy(self.pre_build)
        self.debug()
        self.rollback_status()
        self.debug()

    def debug(self):
        super().debug_status()

    def level_up(self, count=1):
        super().level_up(count)
        self.refresh_rune()
