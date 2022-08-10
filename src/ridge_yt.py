#データの前処理

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


#日付毎に{train, test}に分ける
def split_day(df, test_size, random_state):
    """データを日付別に{train, test}に分ける

    Args:
        df (pandas.core.frame.DataFrame): pandas"DataFrame"型のデータセット
        test_size (float): テストデータの割合
        random_state (int): random_stateの設定値

    Returns:
        _type_: _description_
    """
    X, y = df.iloc[:, [2, 5, 6, 7, 8]], df.iloc[:, 3]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test


#チャンネルごとに{train, test}に分ける
def split_channel(df, X, y, by_index, train_ratio, random_state=0):
    """データをチャンネル毎に{train, test}に分ける

    Args:
        df (pandas.core.frame.DataFrame): pandas"DataFrame"型のデータセット
        X (list): 説明変数のdf内のindex
        y (list): 目的変数のdf内のindex
        by_index (int): どのカラムによってデータを分けるかを指定
        train_ratio (float): 学習データの割合
        random_state (int, 0): チャンネルを分割するときのrandom_state. Defaults to 0.

    Returns:
        _type_: _description_
    """
    print(df.columns[9])
    
    #カラム名を取得
    col_name = df.columns[by_index]

    #指定カラムのユニークな値を取得
    split_by = df.iloc[:, by_index].unique()

    #取得したユニークな値をシャッフル
    split_by = shuffle(split_by, random_state=random_state)
    
    #学習用のチャンネルと教師用のチャンネルを分ける
    train_channel, test_channel = np.split(split_by, [int(split_by.size * train_ratio)])
    print(f"train_channel : {train_channel}")
    print(f"test_channel : {test_channel}")

    #指定されたチャンネルごとに{train,test}に分ける
    df_train = df[df[col_name].isin(train_channel)]
    df_test = df[df[col_name].isin(test_channel)]
    
    #それぞれ使用するcolumnを持つように成形
    X_train = df_train.iloc[:, X]
    y_train = df_train.iloc[:, y]

    X_test = df_test.iloc[:, X]
    y_test = df_test.iloc[:, y]

    return X_train, X_test, y_train, y_test
