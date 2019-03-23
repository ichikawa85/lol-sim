import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
import scipy.optimize
# %matplotlib inline

def func(x, a, b):
    return a*x + b

target_path = "./results/per_version_xp/"
files = os.listdir(target_path)
colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]
# fig = plt.figure(figsize=(10,10))

for i in range(len(files)):
    fig = plt.figure(figsize=(10,10))
    # グラフ作成
    data = pd.read_csv(target_path + files[i])
    data_col = data.columns
    x = data[data_col[0]]
    a, b = np.polyfit(x, data[data_col[1]], 1)
    y = a * x + b
    ax = fig.add_subplot(111)
    ax.scatter(data[data_col[0]], data[data_col[1]])
    ax.plot(x, y, color="b")
    ax.text(0.1,0.9, 'y='+ str(round(a,2)) +'x'+str(round(b,2)), fontsize=18, transform=ax.transAxes)
    print('y='+ str(round(a,2)) +'x'+str(round(b,2)))
    ax.set_xlabel('minute')
    ax.set_ylabel('XP')
    ax.set_xlim(xmin=0)
    ax.set_ylim(ymin=0)

plt.title("Experience(patch 9.1 - 9.5)")
# plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('9.' + str(i+1) + '_xp.png')
# plt.savefig('all_xp_single.png')
