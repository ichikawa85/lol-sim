import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
# %matplotlib inline

target_path = "./results/csv/"
files = os.listdir(target_path)

# グラフ作成
plt.figure(1)

for el in files:
    # try:
    data = pd.read_csv("./results/csv/" + el)
    data_col = data.columns
    timeline = data[data_col[0]].astype('float')
    data = data.sort_values(by="timeline", ascending=True)
    log_data = np.log(data)
    plt.plot(data[data_col[0]],data[data_col[1]],marker='${}$'.format(str(el)))
    # except:
    #     print("Error: Unknown error ")


#グラフの軸
plt.xlabel('minute')
plt.ylabel('AD')

plt.savefig('patch.png')  #pngファイルとして保存
plt.show()
