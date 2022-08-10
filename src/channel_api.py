# -*- coding: utf-8 -*-


import json
import requests
import datetime


class YTstat:
    
    def __init__(self, api_key, channel_id, channel_name):
        """コンストラクタ

        Args:
            api_key (str): YouTube Data API を使用するためのAPIキー
            channel_id (str): 対象となるYouTubeチャンネルのチャンネルID
            channel_name (str): 対象となるYouTubeチャンネルのチャンネル名
        """
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_statistics = None


    #googleapiを用いてチャンネルのデータを取得する
    def get_channel_statistics(self):
        """google apiを用いてチャンネルのデータを取得する

        Returns:
            dictionary: 取得したデータ
        """
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        #不要なデータを捨てる
        try:
            data = data["items"][0]["statistics"]
        except KeyError:
            data = None
            
        
        #登録者数を隠しているかを確認
        if data["hiddenSubscriberCount"]:
            print(f"{self.channel_name}のチャンネル登録者数を取得できません")
            return
        
        #データ型変換
        data["viewCount"] = int(data["viewCount"])
        data["subscriberCount"] = int(data["subscriberCount"])
        data["videoCount"] = int(data["videoCount"])
        
        self.channel_statistics = data
        return data


    #jsonファイルにデータを書き込む
    def dump(self):
        """jsonファイルにデータを書き込む
        """
        if self.channel_statistics is None:
            print("can't dump!!!!!!!!!!!!!")
            return 
        
        
        #保存するファイル名を作成
        channel_title = self.channel_name.replace(" ", "_").lower()
        # channel_title = channel_title.replace("-", "_")
        channel_title = channel_title.replace("/", "_")
        tdy = datetime.date.today()
        file_name = "data/" + channel_title + "-" + str(tdy.month) + "-" + str(tdy.day) + '.json'
        
        with open(file_name, "w") as f:
            json.dump(self.channel_statistics, f, indent=4)
        
        print("file dump")