# dm_G4
## Overview
YouTubeのチャンネル登録者数を予測する

## Requirement
python3.8  
scikit-learn  
numpy  
pandas  
google-api-python-client  
schedule

## Installation
```
pip install google-api-python-client
pip install scikit-learn
pip install numpy 
pip install pandas
pip install schedule
```

## Directory construction
data：YouTube Data APIから収集したデータを入れるディレクトリ  
database：収集したデータをもとにチャンネルごとに構築したデータセットを入れるディレクトリ

```
.
├── data
├── database
└── src
```



## Usage
### 事前準備
"channel_ids.txt"に"チャンネルID チャンネル名"の形式で対象チャンネルを指定する
main.pyの5行目にある変数"API_KEY"にGoogle Consoleから取得したAPIキーを入力する

1.main.pyを実行してデータを収集する
```
python src/main.py
```

2.dataset_make.pyを実行して、収集したデータからデータセットを構築する
```
python src/dataset_make.py
```

3.データから学習を行う
```
python src/learn.py
```

## Note
実行はdm_G4ディレクトリ上でしてください。  



## Author 
氏名：志田晃一
