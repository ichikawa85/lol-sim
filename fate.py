import json
import os
import datetime
from riotwatcher import RiotWatcher, ApiError
from calc import Summoner
import math

class FateAPCalc(object):
    def __init__(self):
        f_item = open("./item/9.6.1/item.json", 'r')
        self.json_item = json.load(f_item)
        self.json_item_data = self.json_item["data"]

    # 各イベントを適用させる
    def apply_events(self, events, summoner, game_id, version): # String events, Summoner summoner
        level_diff = 0
        path_w = './modules/get-data/results/flat_csv/' + game_id + '-' + version + '.csv'
        f = open(path_w, 'a')
        f.write('timeline, ap \n')
        destroy_count = 0
        purchase_count = 0
        json_events = json.loads(json.dumps(events))
        gold_list = [500, 1600, 1900, 2750, 3500, 4300, 5350, 6200, 7050, 7500, 8600, 9500, 10600, 10900, 12150, 13400, 14500, 17500]
        gold_list2 = [400, 1700, 2000, 2850, 3900, 4700, 5750, 6600, 7450, 7900, 9150, 10400, 11500, 12600, 13500, 14100, 14400, 17400]
        count = 0
        roa_time = 0
        roa_bonus = 0
        rabadon_bonus = 1
        for i in range(600):
            t = i/10
            gold = 413.11*t - 310.07
            if roa_time != 0 and roa_bonus < 40:
                roa_bonus = 4*math.floor(t-roa_time)

            try:
                if json_events[count]["type"] in 'ITEM_PURCHASED':
                    item = self.json_item_data[str(json_events[count]["itemId"])]
                    if gold > gold_list2[purchase_count]:
                        summoner.purchase_item(json_events[count]["itemId"])
                        if json_events[count]["itemId"] == 3027: # when RoA purchased
                            roa_time = t
                        if json_events[count]["itemId"] == 3089: # when Rabadon purchased
                            rabadon_bonus = 1.4
                        count+=1
                        purchase_count+=1
                        if json_events[count]["type"] in 'ITEM_DESTROYED':
                            for j in range(count, len(json_events)):
                                # 購入だった場合、何個の素材からアップデートしたかを算出
                                if json_events[j]["type"] is not None:
                                    if json_events[j]["type"] in 'ITEM_DESTROYED':
                                        summoner.sell_item(json_events[count]["itemId"])
                                        count+=1
                                    else:
                                        break

                else:
                    print('An eventType no match.')
            except IndexError as err:
                pass

            # output_str = str(i/10) + ", " + str((round(summoner.magicdamage)+roa_bonus)*rabadon_bonus) + ", " + str(summoner.build) + "\n"
            output_str = str(i/10) + ", " + str((round(summoner.magicdamage)+roa_bonus)*rabadon_bonus) + "\n"
            f.write(output_str)

        f.close()

fate_ap_calc = FateAPCalc()

rune = [0, 0, 0]
version = "9.6.1"
game_id = "11"
summoner = Summoner("TwistedFate", rune, version)
summoner.reflect_rune()
# path = "./event"
# with open(path) as f:
#     event = f.read()
event = [{'timestamp': 4666, 'type': 'ITEM_PURCHASED','level': 1,  'itemId': 2033,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3010,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 1001,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 1026,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3027,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 3010,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 1026,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3111,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 1001,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3057,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3113,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 1026,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3100,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 3057,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 3113,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 1026,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3191,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3108,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 2419,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3157,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 3191,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 3108,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 2419,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 1058,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 1058,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3089,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 1058,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_DESTROYED',  'level': 1,  'itemId': 1058,  'participantId': 6}, {'timestamp': 4666, 'type': 'ITEM_PURCHASED',  'level': 1,  'itemId': 3102,  'participantId': 6}]
event2 = [{'type': 'ITEM_PURCHASED',  'itemId': 1056}, { 'type': 'ITEM_PURCHASED',    'itemId': 3802}, { 'type': 'ITEM_PURCHASED',    'itemId': 1001}, { 'type': 'ITEM_PURCHASED',    'itemId': 1026}, { 'type': 'ITEM_PURCHASED',    'itemId': 3285}, { 'type': 'ITEM_DESTROYED',    'itemId': 3802}, { 'type': 'ITEM_DESTROYED',    'itemId': 1026}, { 'type': 'ITEM_PURCHASED',    'itemId': 3111}, { 'type': 'ITEM_DESTROYED',    'itemId': 1001}, { 'type': 'ITEM_PURCHASED',    'itemId': 3057}, { 'type': 'ITEM_PURCHASED',    'itemId': 3113}, { 'type': 'ITEM_PURCHASED',    'itemId': 1026}, { 'type': 'ITEM_PURCHASED',    'itemId': 3100}, { 'type': 'ITEM_DESTROYED',    'itemId': 3057}, { 'type': 'ITEM_DESTROYED',    'itemId': 3113}, { 'type': 'ITEM_DESTROYED',    'itemId': 1026}, { 'type': 'ITEM_PURCHASED',    'itemId': 1058}, { 'type': 'ITEM_PURCHASED',    'itemId': 1058}, { 'type': 'ITEM_PURCHASED',    'itemId': 3089}, { 'type': 'ITEM_DESTROYED',    'itemId': 1058}, { 'type': 'ITEM_DESTROYED',    'itemId': 1058}, { 'type': 'ITEM_PURCHASED',    'itemId': 3191}, { 'type': 'ITEM_PURCHASED',    'itemId': 3108}, { 'type': 'ITEM_PURCHASED',    'itemId': 2419}, { 'type': 'ITEM_PURCHASED',    'itemId': 3157}, { 'type': 'ITEM_DESTROYED',    'itemId': 3191}, { 'type': 'ITEM_DESTROYED',    'itemId': 3108}, { 'type': 'ITEM_DESTROYED',    'itemId': 2419}, { 'type': 'ITEM_PURCHASED',    'itemId': 3102}, { 'type': 'ITEM_DESTROYED',    'itemId': 1056}]
fate_ap_calc.apply_events(event2, summoner, game_id, version)
