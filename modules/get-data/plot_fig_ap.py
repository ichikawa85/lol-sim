import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
import math
# %matplotlib inline

def xp2level(xp):
    level = 0
    require_xp = [
        0,
        280,
        660,
        1140,
        1720,
        2400,
        3180,
        4060,
        5040,
        6120,
        7300,
        8580,
        9960,
        11440,
        13020,
        14700,
        16480,
        18360,
        100000
    ]
    
    for i in range(len(require_xp)-1):
        if require_xp[i] <= xp and xp < require_xp[i+1]:
            return i+1

    if level == 0:
        if xp < 0:
            return 1
        elif xp > 18360:
            return 18

def q_damage(lv):
    skill_level=0
    get_q_level=[1,4,5,7,9]
    q_damage_list = [60,105,150,195,240]
    for level in get_q_level:
        if lv >= level:
            skill_level+=1

    return q_damage_list[skill_level-1]

def w_damage(lv):
    skill_level=0
    get_w_level=[1,8,10,12,13]
    w_damage_list = [90,135,180,225,270]
    for level in get_w_level:
        if lv >= level:
            skill_level+=1

    if skill_level == 0:
        return 0
    else:
        return w_damage_list[skill_level-1]

def base_ad(lv):
    return 68+3.3*(lv-1)*(0.685+0.0175*lv)

def minion_hp(time):
    update = 0
    # ミニオンが1.05分に出現するため1分引いておく
    time = time - 1.0
    hp = [296, 302, 308, 314, 320, 328.25, 336, 344.75, 353, 361.25, 369.5, 377.75, 386, 394.25, 402.5, 410.75, 419, 427.25, 435.5, 443.75, 452, 460.25, 468.5, 476.75, 485]
    if time < 0 :
        time = 0.0
    count = math.floor(time/1.5)
    if count > 24:
        count = 24
    
    return hp[count]

temp_x = []
temp_y = []
temp_y2 = []
temp_y3 = []
temp_y4 = []

temp_ap = []
temp_ap2 = []

all_ar = []
colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]

# times = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
# for j in range(160):
#     all_ar.append(j)
data_list = pd.read_csv("results/flat_csv/3-9.6.1.csv").values.tolist()
data_list2 = pd.read_csv("results/flat_csv/11-9.6.1.csv").values.tolist()
for data in data_list:
    temp_ap.append(data[1])
for data2 in data_list2:
    temp_ap2.append(data2[1])

mr = 0
for i in range(600):
    t = i/10
    hp = minion_hp(t)
    xp = 517.74*t-697.46
    lv = xp2level(xp)
    q = q_damage(lv)
    # print(hp)
    # print(lv)
    # print(q)
    ap = (hp*(100+mr)-100*q)/65
    ap2 = (hp*(100+mr)-100*q*1.06)/math.floor(65*1.06)
    ap3 = (hp*(100+mr)-100*q*1.09)/math.floor(65*1.09)
    ap4 = (hp*(100+mr)-100*q*1.12)/math.floor(65*1.12)
    print(t)
    print(ap)
    temp_x.append(t)
    temp_y.append(ap)
    temp_y2.append(ap2)
    temp_y3.append(ap3)
    temp_y4.append(ap4)


fig = plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 18

x = np.array(temp_x)
y = np.array(temp_y)
y2 = np.array(temp_y2)
y3 = np.array(temp_y3)
y4 = np.array(temp_y4)
ap = np.array(temp_ap)
ap2 = np.array(temp_ap2)

ax = fig.add_subplot(1, 1, 1)
ax.plot(x, y,color=colorlist[0], label='unused', linestyle="dashed")
ax.plot(x, y2,color=colorlist[1], label='1-time use', linestyle="dashed")
ax.plot(x, y3,color=colorlist[2], label='2-times use', linestyle="dashed")
ax.plot(x, y4,color=colorlist[3], label='3-times use', linestyle="dashed")
# ax.plot(x, y,color=colorlist[0], label='unused')
# ax.plot(x, y2,color=colorlist[1], label='1-time use')
# ax.plot(x, y3,color=colorlist[2], label='2-times use')
# ax.plot(x, y4,color=colorlist[3], label='3-times use')
ax.plot(x, ap,color=colorlist[4], label='AP(RoA)', linewidth=3)
ax.plot(x, ap2,color=colorlist[5], label='AP(Echo)', linewidth=3)
ax.set_xlabel('minute')
ax.set_ylabel('AP')
plt.title("Require Ability Power")
ax.set_xlim(xmin=0)
# ax.set_ylim(ymin=0)
plt.legend(loc='lower right')
# plt.tight_layout()
plt.savefig('require_ap_echo.png')
plt.show()
