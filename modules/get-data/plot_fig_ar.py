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
    get_w_level=[2,8,10,12,13]
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
    hp = [296, 302, 308, 314, 320, 328.25, 336, 344.75, 353, 361.25, 369.5, 377.75, 386, 394.25, 402.5, 410.75, 419, 427.25, 435.5, 443.75, 452, 460.25, 468.5, 476.75, 485]
    # f time%1.5 == 0:
    count = math.floor(time/1.5)
    
    return hp[count]

temp_x = []
temp_y = []

all_ar = []
# times = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
# for j in range(160):
#     all_ar.append(j)

temp_lv = 0
for i in range(60):
    t = i
    ad = 6.08*t-13.25
    xp = 484.85*t-1015.85
    lv = xp2level(xp)
    if temp_lv != lv:
        for j in range(160):
            times[lv-1].append(t)
    temp_lv = lv
    q = q_damage(lv)
    w = w_damage(lv)
    b = base_ad(lv)
    ar = (40*ad+630*lv+210)/(0.27*ad+0.1*q+0.1*w+0.1*b+0.252*lv+1.908)
    # print(40*ad+630*lv+210)
    temp_x.append(t)
    temp_y.append(ar)

fig = plt.figure(figsize=(10,10))

x = np.array(temp_x)
y = np.array(temp_y)

ax = fig.add_subplot(1, 1, 1)
# for t in times:
#     ax.plot(t, all_ar)
ax.plot(x, y)
ax.set_xlabel('minute')
ax.set_ylabel('AR')
plt.title("Require Armor(patch 9.1 - 9.5)")
ax.set_xlim([0, 60])
# ax.set_ylim([0, 550])
# plt.legend(loc='lower right')
# plt.tight_layout()
# plt.savefig('require_ar2.png')
plt.show()
