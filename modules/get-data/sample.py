# -*- coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

def main():
    # 要素の順序反転
    f = [1,3,7,10]
    
    #　x軸の生成
    x = np.linspace(1, len(f), len(f))
    
    #　フィッティング
    a1, a2, b = np.polyfit(x, f, 2)
    
    # フィッティング曲線
    fh = a1 * x**2 + a2 * x + b
    
    # 日経平均株価のプロット
    plt.plot(x, f,  label="f")

    # フィッティング曲線のプロット
    plt.plot(x, fh, label="fh")

    #　グラフの各種設定
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
