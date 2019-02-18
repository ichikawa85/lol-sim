import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# %matplotlib inline

# グラフ作成
plt.figure(1)

for i in range(5):
    try:
        data = pd.read_csv("./results/csv/{}.csv".format(i))
        data_col = data.columns
        timeline = data[data_col[0]].astype('float')
        data = data.sort_values(by="timeline", ascending=True)
        log_data = np.log(data)
        plt.plot(data[data_col[0]],data[data_col[1]],marker='${}$'.format(str(i)))
    except:
        print("Error: Unknown error ")


#グラフの軸
plt.xlabel('timeline')
plt.ylabel('AD')

plt.savefig('result3.png')  #pngファイルとして保存
plt.show()
