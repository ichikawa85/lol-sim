import json
import os
import datetime
from riotwatcher import RiotWatcher, ApiError
from calc import Summoner

SOLO_QUEUE = 'RANKED_SOLO_5x5'
TEAM_QUEUE = 'RANKED_TEAM_5x5'
PARTICIPANTS_SIZE = 10
TARGET_CHAMPION = 4
SUMMONERS_RIFT = 420
SEASON_NUMBER = 13 # means season9

class DataManager(object):
    def __init__(self):
        self.watcher = RiotWatcher('RGAPI-6465675b-768f-4922-8810-45b3ae727468')
        self.my_region = 'jp1'
        # self.today = datetime.datetime.today().strftime("%Y%m%d")
        self.today = "20190329"
        self.match_path = './modules/get-data/jsons/fate_match/'
        self.timeline_path = './modules/get-data/jsons/fate_match_timeline/'
        self.description_path = './modules/get-data/jsons/fate_match_desc/'
        if os.path.exists(self.match_path) is False:
            os.mkdir(self.match_path)
        if os.path.exists(self.timeline_path) is False:
            os.mkdir(self.timeline_path)
        if os.path.exists(self.description_path) is False:
            os.mkdir(self.description_path)

        self.marksman_list = self.get_role_key_list("Marksman", "9.6.1")

    
    def get_over_master_rank_summoner(self):
        master = self.watcher.league.masters_by_queue(self.my_region, SOLO_QUEUE)
        grandmaster = self.watcher.league.grandmaster_by_queue(self.my_region, SOLO_QUEUE)
        challenger = self.watcher.league.challenger_by_queue(self.my_region, SOLO_QUEUE)

        target_path = "modules/get-data/jsons/master/"+ self.today
        if os.path.exists(target_path) is False:
            os.mkdir(target_path)
        path1 = target_path +"/master.json"
        with open(path1, mode='w') as f:
            f.write(str(master))
        path2 = target_path +"/grandmaster.json"
        with open(path2, mode='w') as f:
            f.write(str(grandmaster))
        path3 = target_path +"/challenger.json"
        with open(path3, mode='w') as f:
            f.write(str(challenger))

    # サモナー名から特定のチャンピオンを使った場合の試合データ取得
    def get_match(self):
        count=0
        entries = []
        master = open("./modules/get-data/jsons/master/"+self.today+"/master.json", 'r')
        grandmaster = open("./modules/get-data/jsons/master/"+self.today+"/grandmaster.json", 'r')
        challenger = open("./modules/get-data/jsons/master/"+self.today+"/challenger.json", 'r')
        master_data = json.load(master)
        grandmaster_data = json.load(grandmaster)
        challenger_data = json.load(challenger)
        master_entries = master_data["entries"]
        grandmaster_entries = grandmaster_data["entries"]
        challenger_entries = challenger_data["entries"]
        entries.extend(master_entries)
        entries.extend(grandmaster_entries)
        entries.extend(challenger_entries)
        print(entries)

        master.close()
        grandmaster.close()
        challenger.close()

        for i in range(len(entries)):
            summoner_name = entries[i]["summonerName"]
            print(summoner_name)
            summoner_info = self.watcher.summoner.by_name(self.my_region, summoner_name)
            try:
                _match = self.watcher.match.matchlist_by_account(self.my_region, summoner_info["accountId"], queue=SUMMONERS_RIFT, champion=TARGET_CHAMPION, season=SEASON_NUMBER)
                path = self.match_path + str(count) + ".json"
                with open(path, mode='w') as f:
                    f.write(str(_match))
                count+=1
            except ApiError as err:
                if err.response.status_code == 404:
                    print('Not found.')
                    pass
                else:
                    print('An error has occured.')

        print("End Script.")

    def get_game_id(self):
        target_path = self.match_path
        match_game_id_list = []
        files = os.listdir(target_path)
        for i in range(len(files)):
            f = open(target_path + str(i) + ".json", 'r')
            data = json.load(f)
            for j in range(len(data["matches"])):
                match_game_id_list.append(data["matches"][j]["gameId"])
                
        with open("./modules/get-data/jsons/game_id_list", mode='w') as f:
            f.write(str(match_game_id_list))
        return match_game_id_list

    def get_game_timeline(self):
        game_id_list = self.get_game_id()
        for game_id in game_id_list:
            print(game_id)
            try:
                match_timeline = self.watcher.match.timeline_by_match(self.my_region, game_id)
                path_w = self.timeline_path + game_id + '.json'
                with open(path_w, mode='w') as ff:
                    ff.write(str(match_timeline))
            except:
                print("Error: Unknown error ")


    def get_game_description(self):
        game_id_list = self.get_game_id()
        for game_id in game_id_list:
            try:
                path_w = self.description_path + game_id + '.json'
                match_description = self.watcher.match.by_id(self.my_region, game_id)
                with open(path_w, mode='w') as ff:
                    ff.write(str(match_description))
            except:
                print("Error: Unknown error ")

    def get_game_version(self, file_path):
        print(file_path)
        f = open(file_path, 'r')
        json_data = json.load(f)
        version = json_data["gameVersion"]
        f.close()
        return version

    # 特定のチャンピオンに絞った結果を取得
    def get_events_limited_the_champion(self, game_id):
        # match_index=1
        level = 0
        participant_id = self.get_participant_id(TARGET_CHAMPION, game_id)
        target_path = self.timeline_path + game_id + '.json'
        f = open(target_path, 'r')
        json_data = json.load(f)
        ret_events = []

        print(participant_id)
        for frame in range(len(json_data["frames"])):
            level = json_data["frames"][frame]["participantFrames"][str(participant_id)]["level"]
            for j in range(len(json_data["frames"][frame]["events"])):
                events = json.loads(json.dumps(json_data["frames"][frame]["events"][j]))
                try:
                    if events["participantId"] == participant_id:
                        events["level"] = level
                        ret_events.append(events)
                        
                except KeyError as err:
                    # print("KeyError")
                    pass

        return ret_events

    # 特定のチャンピオンのxp経緯を取得
    def get_xp_timeline(self, game_id, version):
        participant_id = self.get_participant_id(TARGET_CHAMPION, game_id)
        target_path = self.timeline_path + game_id + '.json'
        f = open(target_path, 'r')
        json_data = json.load(f)
        ret_events = []

        path_w = './modules/get-data/results/xp_csv/' + game_id + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, xp, game_id \n')
        first_flag = True

        for frame in range(len(json_data["frames"])):
            
            timestamp = json_data["frames"][frame]["timestamp"]
            min_timestamp = round((timestamp) / 1000 / 60, 1)
            xp = json_data["frames"][frame]["participantFrames"][str(participant_id)]["xp"]
            output_str = str(min_timestamp) + ', ' +str(xp) + ', ' + game_id + "\n"
            f.write(output_str)
            
        f.close()

    # 特定のチャンピオンの対面との経験値の差分の累積を取得
    def get_xp_diff(self, game_id, version):
        participant_id = self.get_participant_id(TARGET_CHAMPION, game_id)
        opposive_participant_id = self.get_opposive_participant_id(TARGET_CHAMPION, game_id, self.marksman_list)
        if opposive_participant_id == -1:
            return -1
        target_path = self.timeline_path + game_id + '.json'
        f = open(target_path, 'r')
        json_data = json.load(f)
        commulation = 0

        path_w = './modules/get-data/results/xp_diff_csv/' + game_id + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, xp_diff, game_id \n')
        first_flag = True

        for frame in range(len(json_data["frames"])):     
            timestamp = json_data["frames"][frame]["timestamp"]
            min_timestamp = round((timestamp) / 1000 / 60, 1)
            xp = json_data["frames"][frame]["participantFrames"][str(participant_id)]["xp"]
            o_xp = json_data["frames"][frame]["participantFrames"][str(opposive_participant_id)]["xp"]
            diff = xp - o_xp
            commulation = commulation + diff
            
        f.close()
        return commulation

    def get_gold_timeline(self, game_id, version):
        participant_id = self.get_participant_id(TARGET_CHAMPION, game_id)
        target_path = self.timeline_path + game_id + '.json'
        f = open(target_path, 'r')
        json_data = json.load(f)
        ret_events = []

        path_w = './modules/get-data/results/gold_csv/' + game_id + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, gold, game_id \n')
        first_flag = True

        for frame in range(len(json_data["frames"])):
            
            timestamp = json_data["frames"][frame]["timestamp"]
            min_timestamp = round((timestamp) / 1000 / 60, 1)
            gold = json_data["frames"][frame]["participantFrames"][str(participant_id)]["totalGold"]
            output_str = str(min_timestamp) + ', ' +str(gold) + ', ' + game_id + "\n"
            f.write(output_str)
            
        f.close()

    def get_gold_diff(self, game_id, version):
        participant_id = self.get_participant_id(TARGET_CHAMPION, game_id)
        opposive_participant_id = self.get_opposive_participant_id(TARGET_CHAMPION, game_id, self.marksman_list)
        if opposive_participant_id == -1:
            return -1
        target_path = self.timeline_path + game_id + '.json'
        f = open(target_path, 'r')
        json_data = json.load(f)
        commulation = 0

        for frame in range(len(json_data["frames"])):
            timestamp = json_data["frames"][frame]["timestamp"]
            min_timestamp = round((timestamp) / 1000 / 60, 1)
            gold = json_data["frames"][frame]["participantFrames"][str(participant_id)]["totalGold"]
            o_gold = json_data["frames"][frame]["participantFrames"][str(opposive_participant_id)]["totalGold"]
            diff = gold - o_gold
            commulation = commulation + diff

        f.close()
        return commulation
        
    # 指定したチャンピオンの参加者IDの取得
    def get_participant_id(self, champion_id, game_id):
        desc_path = self.description_path + game_id + '.json'
        desc = open(desc_path, 'r')
        json_data = json.load(desc)
        participant_id = -1
        for j in range(PARTICIPANTS_SIZE):
            _champion_id = json_data["participants"][j]["championId"]
            if _champion_id == champion_id:
                participant_id = json_data["participants"][j]["participantId"]

        desc.close()
        return participant_id

    # 対面の参加者IDの取得
    def get_opposive_participant_id(self, champion_id, game_id, marksman_list):
        desc_path = self.description_path + game_id + '.json'
        desc = open(desc_path, 'r')
        json_data = json.load(desc)
        participant_id = self.get_participant_id(champion_id, game_id)
        ret = -1

        lane = ""
        opposive_team_id = 0
        for j in range(PARTICIPANTS_SIZE):
            _participant_id = json_data["participants"][j]["participantId"]
            if participant_id == _participant_id:
                lane = json_data["participants"][j]["timeline"]["lane"]
                team_id = json_data["participants"][j]["teamId"]
                if team_id == 100:
                    opposive_team_id = 200
                elif team_id == 200:
                    opposive_team_id = 100
                else:
                    print("Error: Team ID value")
                    
        for j in range(PARTICIPANTS_SIZE):
            if json_data["participants"][j]["teamId"] == opposive_team_id and lane in json_data["participants"][j]["timeline"]["lane"] and lane not in "NONE" and str(json_data["participants"][j]["championId"]) not in marksman_list and json_data["participants"][j]["timeline"]["role"] not in "DUO_SUPPORT":

                ret = json_data["participants"][j]["participantId"]
                        
        desc.close()
        return ret

    # 指定したロールのチャンピオンリストを返す
    def get_role_key_list(self, role, version):
        champions_path = 'champions/' + version + '/'
        files = os.listdir(champions_path)
        key_list = []
        for file in files:
            name = file.split(".")[0]
            f = open("./champions/" + version + "/" + file, 'r')
            champion_data = json.load(f)
            tag = champion_data["data"][name]["tags"]
            if role in tag:
                key_list.append(champion_data["data"][name]["key"])
            f.close()

        return key_list

    # 各イベントを適用させる
    def apply_events(self, events, summoner, game_id, version): # String events, Summoner summoner
        json_events_with_item = json.loads(json.dumps(events))
        level_diff = 0
        path_w = './modules/get-data/results/flat_csv/' + game_id + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, ap, lv, game_id \n')
        destroy_count = 0
        events_without_consumption_item = []
        for event in json_events_with_item:
            try:
                # Delete control ward, potion, Refillable Potion
                if event["itemId"] == 2055 or event["itemId"] == 2003 or event["itemId"] == 2031:
                    pass
                else:
                    events_without_consumption_item.append(event)
            except KeyError as err:
                events_without_consumption_item.append(event)

        json_events = json.loads(json.dumps(events_without_consumption_item))
        lv = 1
            
        for i in range(len(json_events)):
            if json_events[i]["type"] in 'ITEM_PURCHASED':
                summoner.purchase_item(json_events[i]["itemId"])
            elif json_events[i]["type"] in 'ITEM_SOLD':
                summoner.sell_item(json_events[i]["itemId"])
            elif json_events[i]["type"] in 'ITEM_DESTROYED':
                summoner.sell_item(json_events[i]["itemId"])
            elif json_events[i]["type"] in 'ITEM_UNDO':
                summoner.undo_item()
            elif json_events[i]["type"] in 'SKILL_LEVEL_UP':
                if json_events[i]["skillSlot"] == 1:
                    summoner.q_up()
                elif json_events[i]["skillSlot"] == 2:
                    summoner.w_up()
                elif json_events[i]["skillSlot"] == 3:
                    summoner.e_up()
                elif json_events[i]["skillSlot"] == 4:
                    summoner.r_up()
                # # minute (level output)
                # min_timestamp = round(json_events[i]["timestamp"] / 1000 / 60, 1)
                # output_str = str(min_timestamp) + ", " + str(lv) + "\n"
                # f.write(output_str)
                # lv+=1
            else:
                print('An eventType no match.')

            # level manage
            summoner.level_up_to(json_events[i]["level"])

            # minute
            min_timestamp = round(json_events[i]["timestamp"] / 1000 / 60, 1)

            # output
            if json_events[i]["type"] in 'ITEM_PURCHASED':
                for j in range(i+1, len(json_events)):
                    # 購入だった場合、何個の素材からアップデートしたかを算出
                    if json_events[j]["type"] is not None:
                        if json_events[j]["type"] in 'ITEM_DESTROYED':
                            destroy_count+=1
                        else:
                            break

            if destroy_count == 0:
                output_str = str(min_timestamp) + ", " + str(round(summoner.magicdamage)) + ", " + str(summoner.level) + ", " + game_id + "\n"
                f.write(output_str)
            else:
                destroy_count-=1

        f.close()

    def decision_darkin_or_shadow(self, events):
        json_events = json.loads(json.dumps(events))
        shadow_flag = False
        darkin_flag = False
        ret = ''
        for i in range(len(json_events)):
            if json_events[i]["type"] in 'ITEM_PURCHASED':
                if json_events[i]["itemId"] == 3134 or json_events[i]["itemId"] == 3147 or json_events[i]["itemId"] == 3142:
                    shadow_flag = True
                elif json_events[i]["itemId"] == 3071 or json_events[i]["itemId"] == 3044 or json_events[i]["itemId"] == 3053 or json_events[i]["itemId"] == 3052:
                    darkin_flag = True

        if darkin_flag is False and shadow_flag is False:
            for i in range(len(json_events)):
                if json_events[i]["type"] in 'ITEM_PURCHASED':
                    if json_events[i]["itemId"] == 3117:
                        shadow_flag = True
                    elif json_events[i]["itemId"] == 3047:
                        darkin_flag = True

        if darkin_flag is True and shadow_flag is True:
            for i in range(len(json_events)):
                if json_events[i]["type"] in 'ITEM_PURCHASED':
                    if json_events[i]["itemId"] == 3053 or json_events[i]["itemId"] == 3065 or json_events[i]["itemId"] == 3211:
                        shadow_flag = False
                    elif json_events[i]["itemId"] == 3142:
                        darkin_flag = False

        if shadow_flag is True:
            ret = ret + 'shadow'

        if darkin_flag is True:
            ret = ret + 'darkin'

        return ret

    def update_match_data(self):
        # self.get_over_master_rank_summoner()
        ### !!! We need to organize json format at here.
        # self.get_match()
        self.get_game_description()
        self.get_game_timeline()
        
    def output_csv(self):
        version = ''
        target_path = self.timeline_path
        files = os.listdir(target_path)
        num = len(os.listdir(target_path))
        desc_path = self.description_path

        path_w = './modules/get-data/results/diff-commulation.csv'
        f = open(path_w, 'a')
        f.write('xp_diff, gold_diff, game_id \n')

        rune = [0, 0, 0]
        for file in files:
            try:
                game_id = file.split(".")[0]
                json_path = self.description_path + game_id + ".json"
                version_array = self.get_game_version(json_path).split('.') # ['7', '19', '203', '1070']
                version = version_array[0] + "." + version_array[1] + ".1"

                if '9' in version_array[0]: # only season9
                    # summoner = Summoner("TwistedFate", rune, version)
                    # summoner.reflect_rune()
                    # events = self.get_events_limited_the_champion(game_id)
                    # self.apply_events(events, summoner, game_id, version)
                    # summoner = None
                    # self.get_xp_timeline(game_id, version)
                    # self.get_gold_timeline(game_id, version)
                    xp_diff = self.get_xp_diff(game_id, version)
                    gold_diff = self.get_gold_diff(game_id, version)
                    if xp_diff == -1 or gold_diff == -1:
                        pass
                    else:
                        output_str = str(xp_diff) + ', ' +str(gold_diff) + ', ' + game_id + "\n"
                        f.write(output_str)

                else:
                    pass
            
            except KeyError as err:
                print("Error: KeyError")
                
        f.close()

data_manager = DataManager()    
data_manager.output_csv()
# data_manager.update_match_data()

# rune = [0, 0, 0]
# version = "9.6.1"
# game_id = "1"
# summoner = Summoner("TwistedFate", rune, version)
# summoner.reflect_rune()
# events = data_manager.get_events_limited_the_champion("190183934")
# print(events)
# data_manager.self.apply_events(events, summoner, game_id, version)
