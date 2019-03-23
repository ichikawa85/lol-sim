import json
import os
from riotwatcher import RiotWatcher, ApiError
from calc import Summoner

SOLO_QUEUE = 'RANKED_SOLO_5x5'
TEAM_QUEUE = 'RANKED_TEAM_5x5'
PARTICIPANTS_SIZE = 10

class DataManager(object):
    def __init__(self):
        self.watcher = RiotWatcher('RGAPI-87627c7d-4c88-405b-b23c-8d8d8789913b')
        self.my_region = 'jp1'
    
    def get_master_rank_summoner(self):
        result = self.watcher.league.masters_by_queue(self.my_region, SOLO_QUEUE)
        path = "modules/get-data/jsons/master/master.json"
        with open(path, mode='w') as f:
            f.write(str(result))

    def get_grandmaster_rank_summoner(self):
        result = self.watcher.league.grandmaster_by_queue(self.my_region, SOLO_QUEUE)
        path = "modules/get-data/jsons/master/grandmaster.json"
        with open(path, mode='w') as f:
            f.write(str(result))

    def get_challenger_rank_summoner(self):
        result = self.watcher.league.challenger_by_queue(self.my_region, SOLO_QUEUE)
        path = "modules/get-data/jsons/master/challenger.json"
        with open(path, mode='w') as f:
            f.write(str(result))

    # サモナー名から特定のチャンピオンを使った場合の試合データ取得
    def get_match(self):
        count=0
        entries = []
        master = open("./modules/get-data/jsons/master/master.json", 'r')
        grandmaster = open("./modules/get-data/jsons/master/grandmaster.json", 'r')
        challenger = open("./modules/get-data/jsons/master/challenger.json", 'r')
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
                _match = self.watcher.match.matchlist_by_account(self.my_region, summoner_info["accountId"], queue=420, champion=141)
                path = "modules/get-data/jsons/kayn_match/" + str(count) + ".json"
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
        target_path = "./modules/get-data/jsons/kayn_match/"
        match_game_id_list = []
        files = os.listdir(target_path)
        for i in range(len(files)):
            f = open("./modules/get-data/jsons/kayn_match/" + str(i) + ".json", 'r')
            data = json.load(f)
            for j in range(len(data["matches"])):
                match_game_id_list.append(data["matches"][j]["gameId"])
                
        with open("./modules/get-data/jsons/game_id_list", mode='w') as f:
            f.write(str(match_game_id_list))
        return match_game_id_list

    def get_game_detail(self):
        game_id_list = self.get_game_id()
        i=0
        for game_id in game_id_list:
            print(game_id)
            try:
                match_detail = self.watcher.match.timeline_by_match(self.my_region, game_id)
                path_w = './modules/get-data/jsons/kayn_match_detail/' + str(i) + '.json'
                with open(path_w, mode='w') as ff:
                    ff.write(str(match_detail))
                    i+=1
            except:
                print("Error: Unknown error ")


    def get_game_description(self):
        game_id_list = self.get_game_id()
        i=0
        for game_id in game_id_list:
            # print(match_id.strip())
            path_w = './modules/get-data/jsons/kayn_match_desc/' + str(i) + '.json'
            match_detail = self.watcher.match.by_id(self.my_region, game_id)
            with open(path_w, mode='w') as ff:
                ff.write(str(match_detail))
            i+=1

    def get_game_version(self, file_path):
        f = open(file_path, 'r')
        json_data = json.load(f)
        version = json_data["gameVersion"]
        f.close()
        return version

    # 特定のチャンピオンに絞った結果を取得
    def get_game_timeline(self, match_index):
        # match_index=1
        level = 0
        participant_id = self.get_participant_id(141, match_index)
        detail_path = './modules/get-data/jsons/kayn_match_detail/' + str(match_index) + '.json'
        f = open(detail_path, 'r')
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
    def get_xp_timeline(self, match_index, version):
        participant_id = self.get_participant_id(141, match_index)
        detail_path = './modules/get-data/jsons/kayn_match_detail/' + str(match_index) + '.json'
        f = open(detail_path, 'r')
        json_data = json.load(f)
        ret_events = []

        path_w = './modules/get-data/results/xp_csv/' + str(match_index) + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, xp \n')
        first_flag = True

        for frame in range(len(json_data["frames"])):
            
            timestamp = json_data["frames"][frame]["timestamp"]
            min_timestamp = round((timestamp) / 1000 / 60, 1)
            xp = json_data["frames"][frame]["participantFrames"][str(participant_id)]["xp"]
            output_str = str(min_timestamp) + ', ' +str(xp) + "\n"
            f.write(output_str)
            
        f.close()

    # 指定したチャンピオンの参加者IDの取得
    def get_participant_id(self, champion_id, index):
        desc_path = './modules/get-data/jsons/kayn_match_desc/' + str(index) + '.json'
        desc = open(desc_path, 'r')
        json_data = json.load(desc)
        participant_id = -1
        for j in range(PARTICIPANTS_SIZE):
            _champion_id = json_data["participants"][j]["championId"]
            if _champion_id == champion_id:
                participant_id = json_data["participants"][j]["participantId"]

        desc.close()
        return participant_id

    # 各イベントを適用させる
    def apply_events(self, events, summoner, match_index, version): # String events, Summoner summoner
        json_events_with_item = json.loads(json.dumps(events))
        level_diff = 0
        # tail = self.decision_darkin_or_shadow(events)
        path_w = './modules/get-data/results/flat_csv/' + str(match_index) + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, ad, lv \n')
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
                output_str = str(min_timestamp) + ", " + str(round(summoner.FlatPhysicalDamageMod)) + ", " + str(summoner.level) + "\n"
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
        # self.get_master_rank_summoner()
        # self.get_grandmaster_rank_summoner()
        # self.get_challenger_rank_summoner()
        ### !!! We need to organize json format at here.
        # self.get_match()
        # self.get_game_description()
        self.get_game_detail()
        
    def output_csv(self):
        version = ''
        target_path = "./modules/get-data/jsons/kayn_match_detail/"
        desc_path = "./modules/get-data/jsons/kayn_match_desc/"
        num = len(os.listdir(target_path))

        rune = [0, 0, 0]
        for i in range(num):
            try:
                json_path = "./modules/get-data/jsons/kayn_match_desc/" + str(i) + ".json"
                version_array = self.get_game_version(json_path).split('.') # ['7', '19', '203', '1070']
                version = version_array[0] + "." + version_array[1] + ".1"

                if '9' in version_array[0]: # only season9
                    summoner = Summoner("Kayn", rune, version)
                    summoner.reflect_rune()
                    events = self.get_game_timeline(i)
                    self.apply_events(events, summoner, i, version)
                    summoner = None
                    # self.get_xp_timeline(i, version)
                else:
                    pass
            
            except KeyError as err:
                print("Error: KeyError")
                os.remove('./modules/get-data/results/csv/' + str(i) + '-' + version+ '.csv')
            # except:
            #     print("Error: Unknown error ")


data_manager = DataManager()
data_manager.output_csv()
# data_manager.update_match_data()

# target_path = "./modules/get-data/jsons/kayn_match_detail/"
# num = len(os.listdir(target_path))
# rune = [0, 0, 0]
# for i in range(num):
#     data_manager.get_xp_timeline(i)
