import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 8))
for param in [format(i, '.1f') for i in range(5)]:  # ここのformat文重要
    df = pd.read_csv('time_series(parameter={}).csv'.format(param))
    ax = fig.add_subplot(111)
    ax.scatter(df['time'], df['Fraction of Cooperation'], label='Parameter ={}'.format(param))
    ax.set_xlabel('Time step')
    ax.set_ylabel('Fraction of Cooperation')
    ax.set_xlim([0, 300])
plt.legend()
plt.tight_layout()
plt.savefig('time_series_data.png')
plt.show()
