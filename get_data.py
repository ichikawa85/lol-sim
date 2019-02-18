import json
import os
from riotwatcher import RiotWatcher, ApiError
from calc import Summoner

SOLO_QUEUE = 'RANKED_SOLO_5x5'
TEAM_QUEUE = 'RANKED_TEAM_5x5'
PARTICIPANTS_SIZE = 10

class DataManager(object):
    def __init__(self):
        self.watcher = RiotWatcher('RGAPI-9e50b96d-b4e2-4f84-8295-e7657b002173')
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

    # サモナー名から特定のチャンピオンを使った場合の試合データ取得
    def get_match(self):
        count=0
        f = open("./modules/get-data/jsons/master/master.json", 'r')
        data = json.load(f)
        entries = data["entries"]

        for i in range(len(entries)):
            summoner_name = data["entries"][i]["summonerName"]
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
        match_game_id_list = []
        for i in range(56):
            f = open("./modules/get-data/jsons/kayn_match/" + str(i) + ".json", 'r')
            data = json.load(f)
            for j in range(len(data["matches"])):
                match_game_id_list.append(data["matches"][j]["gameId"])
        return match_game_id_list

    def get_game_detail(self):
        game_id_list = self.get_game_id()
        i=0
        for game_id in game_id_list:
            print(game_id)
            match_detail = self.watcher.match.timeline_by_match(self.my_region, game_id)
            path_w = './modules/get-data/jsons/kayn_match_detail/' + str(i) + '.json'
            with open(path_w, mode='w') as ff:
                ff.write(str(match_detail))
            i+=1

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
    def apply_events(self, events, summoner, match_index): # String events, Summoner summoner
        json_events = json.loads(json.dumps(events))
        level_diff = 0
        path_w = './modules/get-data/results/csv/' + str(match_index) + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, ad, lv \n')
        destroy_count = 0
            
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
                output_str = str(min_timestamp) + ", " + str(round(summoner.attackdamage)) + ", " + str(summoner.level) + "\n"
                f.write(output_str)
            else:
                destroy_count-=1

        f.close()
            
data_manager = DataManager()
rune = [0, 0, 0]
for i in range(686):
    try:
        summoner = Summoner("Kayn", rune)
        summoner.reflect_rune()
        events = data_manager.get_game_timeline(i)
        data_manager.apply_events(events, summoner, i)
        summoner = None
    except KeyError as err:
        print("Error: KeyError")
        os.remove('./modules/get-data/results/csv/' + str(i) + '.csv')
    except:
        print("Error: Unknown error ")
# data_manager.get_game_description()
# data_manager.get_game_detail()
