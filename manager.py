import json
import time
import threading
import linecache
import csv
from calc import Summoner

class Manager(object):
    def __init__(self):
        self.result = 0
        self.result_list = []
        f = open('result.csv', 'w')
        self.writer = csv.writer(f, lineterminator='\n')

    def timer(self):
        pass

    def level_up(self, target):
        if "1" in target:
            self.summoner1.level_up()
        elif "2" in target:
            self.summoner2.level_up()
            
        pass

    def debug(self):
        print("# -------------")        
        print("# Summoner1")
        print("# -------------")        
        self.summoner1.debug()
        print("# -------------")        
        print("# Summoner2")
        print("# -------------")        
        self.summoner2.debug()

    def one_to_two(self):
        while(1):
            self.summoner1.AA(self.summoner2)
            if self.summoner1.current_hp < 0:
                break
            elif self.summoner2.current_hp < 0:
                print("Summoner1 WIN")
                self.result = 1
                break
        
    def two_to_one(self):
        while(1):
            self.summoner2.AA(self.summoner1)
            if self.summoner2.current_hp < 0:
                break
            elif self.summoner1.current_hp < 0:
                print("Summoner2 WIN")
                self.result = 2
                break

    def start(self, name1, name2):
        self.summoner1 = Summoner(name1)
        self.summoner2 = Summoner(name2)

        #for i in range(10):
        thread1 = threading.Thread(target=self.one_to_two)
        thread2 = threading.Thread(target=self.two_to_one)
        thread1.start()
        thread2.start()

        thread_list = threading.enumerate()
        thread_list.remove(threading.main_thread())
        for thread in thread_list:
            thread.join()

        if self.result == 1:
            self.result_list.append(1)
        elif self.result == 2:
            self.result_list.append(0)

    def match(self):
        # champ_max = 142
        # f = open('result.csv', 'w')
        # writer = csv.writer(f, lineterminator='\n')
        # for i in range(1, champ_max+1):
        #     for j in range(1, champ_max+1):
        #         if i != j:
        #             print("i: "+str(i)+"j: "+str(j))
        #             name1 = linecache.getline('champion-list.txt', i).strip()
        #             name2 = linecache.getline('champion-list.txt', j).strip()
        #         self.manager.start(name1, name2)
        #         else:
        #             pass

        # self.writer.writerow(self.result_list)
        # self.result_list = []
        rune1 = [1, 0, 0]
        rune2 = [0, 1, 2]
        self.summoner1 = Summoner("Yasuo", rune1)
        self.summoner1.debug_status()
        self.summoner2 = Summoner("Yasuo", rune2)
        self.summoner2.debug_status()

        
manager = Manager()
manager.match()
