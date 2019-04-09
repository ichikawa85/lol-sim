import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
# %matplotlib inline

target_path = "./results/"
files = os.listdir(target_path)
colorlist = ["r", "g", "b", "c", "m", "y", "k", "w"]
fig = plt.figure(figsize=(10,10))

# グラフ作成
data = pd.read_csv(target_path + "diff-commulation.csv")
data_col = data.columns
ax = fig.add_subplot(111)
ax.scatter(data[data_col[0]], data[data_col[1]])
ax.set_xlabel('xp commulation')
ax.set_ylabel('gold commulation')
# ax.set_xlim([0,60])
# ax.set_ylim([0,350])

plt.title("Attack Damage(patch 9.1 - 9.6)")
# plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('diff-commulation.png')
