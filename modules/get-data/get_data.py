import json
from riotwatcher import RiotWatcher, ApiError
from calc import Summoner

SOLO_QUEUE = 'RANKED_SOLO_5x5'
TEAM_QUEUE = 'RANKED_TEAM_5x5'
PARTICIPANTS_SIZE = 10

class DataManager(object):
    def __init__(self):
        self.watcher = RiotWatcher('RGAPI-952dccf7-693a-45c8-9efe-4e35ac56b331')
        self.my_region = 'jp1'
    
    def get_master_rank_summoner(self):
        self.result = self.watcher.league.masters_by_queue(my_region, SOLO_QUEUE)
        print(self.result)

    # サモナー名から特定のチャンピオンを使った場合の試合データ取得
    def get_match(self):
        f = open("./jsons/master/master_list_summoner.json", 'r')
        data = json.load(f)
        entries = data["entries"]

        for i in range(len(entries)):
            summoner_name = data["entries"][i]["summonerName"]
            print(summoner_name)
            summoner_info = self.watcher.summoner.by_name(self.my_region, summoner_name)
            try:
                _match = self.watcher.match.matchlist_by_account(self.my_region, summoner_info["accountId"], queue=420, champion=141)
                print(_match)
            except ApiError as err:
                if err.response.status_code == 404:
                    print('Not found.')
                    pass
                else:
                    print('An error has occured.')

        print("End Script.")

    def get_game_id(self):
        for i in range(58):
            f = open("./jsons/kayn_match/" + str(i) + ".json", 'r')
            data = json.load(f)
            for j in range(len(data["matches"])):
                match_game_id = data["matches"][j]["gameId"]
                print(match_game_id)

    def get_game_detail(self):
        f = open('./results/kayn_gameIds', 'r')
        matchId = f.readline()
        i = 0

        while matchId:
            path_w = './jsons/kayn_match_detail/' + str(i) + '.json'
            match_detail = self.watcher.match.timeline_by_match(self.my_region, matchId.strip())
            matchId = f.readline()
            with open(path_w, mode='w') as ff:
                ff.write(str(match_detail))
            i+=1
                
        f.close()

    def get_game_description(self):
        f = open('./results/kayn_gameIds', 'r')
        match_id = f.readline()
        i = 0

        while match_id:
            # print(match_id.strip())
            path_w = './jsons/kayn_match_desc/' + str(i) + '.json'
            match_detail = self.watcher.match.by_id(self.my_region, match_id.strip())
            match_id = f.readline()
            with open(path_w, mode='w') as ff:
                ff.write(str(match_detail))
            i+=1
                
        f.close()

    def get_game_timeline(self):
        match_index=1
        level = 0
        participant_id = self.get_participant_id(141, match_index)
        detail_path = './jsons/kayn_match_detail/' + str(match_index) + '.json'
        f = open(detail_path, 'r')
        json_data = json.load(f)

        print(len(json_data["frames"]))
        for frame in range(len(json_data["frames"])):
            level = json_data["frames"][frame]["participantFrames"][str(participant_id)]["level"]
            for j in range(len(json_data["frames"][frame]["events"])):
                events = json.loads(json.dumps(json_data["frames"][frame]["events"][j]))
                try:
                    if events["participantId"] == participant_id:
                        print("level: " + str(level))
                        print("timestamp: " + str(events["timestamp"]))
                        print("type" + str(events["type"]))
                except KeyError as err:
                    # print("KeyError")
                    pass
                

    def get_participant_id(self, champion_id, index):
        desc_path = './jsons/kayn_match_desc/' + str(index) + '.json'
        desc = open(desc_path, 'r')
        json_data = json.load(desc)
        participant_id = -1
        for j in range(PARTICIPANTS_SIZE):
            champion_id = json_data["participants"][j]["championId"]
            if champion_id == champion_id:
                participant_id = json_data["participants"][j]["participantId"]                

        desc.close()
        return participant_id        
        
            
data_manager = DataManager()
rune = [0, 0, 0]
summoner = Summoner("Kayn", rune)
# data_manager.get_game_timeline()
