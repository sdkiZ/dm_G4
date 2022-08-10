import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
import ridge_yt

def learn():
    """Ridge Regressionモデルを用いた学習と予測精度の測定
    
    """
    
    #対数変換
    df = pd.read_csv("./database/all_channel_diff.csv")
    df["viewCount_Log"] = np.log(df["viewCount"])
    df["subscriberCount_Log"] = np.log(df["subscriberCount"])
    df["videoCount_log"] = np.log(df["videoCount"])
    df["viewCount_diff_log"] = np.log(df["viewCount_diff"])

    #学習実行
    for i in range(10):
        print("-----------{}".format(i))
        X_train, X_test, y_train, y_test = ridge_yt.split_channel(df, X=[ 7, 8, 10, 12, 13], y=[11], by_index=9, train_ratio=0.7, random_state=i) 
        clf = Ridge(alpha=0)
        clf.fit(X_train, y_train)
        print("学習データ score     : {}".format(clf.score(X_train, y_train)))
        print("テストデータ score   : {}".format(clf.score(X_test, y_test)))


if __name__ == "__main__":
    learn()