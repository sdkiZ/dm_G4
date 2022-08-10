import pandas as pd
import json
import glob
import re
import read_data


DATA_PATH = "./data"
DATABASE_PATH = "./database"
COL_TEMP_CSV = ["month", "day", "viewCount", "subscriberCount", "hiddenSubscriberCount", "videoCount"]
COL_TEMP_DB = ["month", "day", "viewCount", "subscriberCount", "hiddenSubscriberCount", "videoCount", "viewCount_diff", "subscriberCount_diff", "videoCount_diff"]



#jsonファイルからチャンネルごとのデータベースを作成してcsv形式に出力
def create_csv(import_path, output_path):
    """jsonファイルからチャンネル毎のデータベースを作成してcsv形式に出力

    Args:
        import_path (str): 処理対象のデータのあるファイルパス
        output_path (str): 処理したデータを保管するファイルパス
    """
    
    #対象チャンネルを読み込む
    channel_ids = read_data.get_channel_data()
    
    #チャンネルごとに操作
    for channel_id in channel_ids:
        channel_name = " ".join(channel_id[1:])
        print(channel_name)


        #チャンネル名整形
        channel_name = channel_name.replace(" ", "_").lower()
        channel_name = channel_name.replace("/", "_")
        channel_name = channel_name.replace("[", "_")
        channel_name = channel_name.replace("]", "_")
        print(channel_name)

        # #チャンネルのDataFrameを作成
        df = pd.DataFrame(columns=COL_TEMP_CSV)


        #チャンネル名のあるjsonファイルを選択
        for file in glob.glob(import_path + "/" + channel_name + "*.json"):

            #選択したjsonファイルの日付を読み取る
            temp = re.findall("-.*j", file)
            day = temp[0][1:-2]

            #jsonファイルを読み込む
            with open(file, "r", encoding="utf-8") as f:
                d = json.load(f)

                #読み込んだjsonファイル用のDataFrame
                df_temp = pd.DataFrame([d])
                
                #DataFrameに日付情報を追加
                df_temp["month"] = day.split("-")[0]
                df_temp["day"] = day.split("-")[1]

                #チャンネルのDataFrameと縦方向に結合
                df = pd.concat([df, df_temp])
                
                #日付順に並べ替える
                df = df.sort_values("day")


        #csv形式に保存
        df.to_csv(output_path + "/" + channel_name + ".csv", index=False)
        
#チャンネルごとのcsvファイルを1日ごとの差分のデータを追加して、一つのcsvファイルにまとめる
#csvファイルを読み込み、1日毎のデータを作成
def create_database(import_path, output_path, column_set=COL_TEMP_DB):
    """チャンネル毎のcsvファイルを"1日毎の差分データ"を追加して1つのcavファイルにまとめる

    Args:
        import_path (str): 処理するデータのファイルパス
        output_path (str): 出力するファイルパス
        column_set (list): 構築するデータセットのカラムセット
    """
    print("開始")
    channels = read_data.get_channel_data()
    channel_counter = 0
    
    df_all = pd.DataFrame(columns=column_set)
    
    for channel in channels:
        channel_name = channel[1]
        channel_name = read_data.conv_channel_name(channel_name)
        print(channel_name)
        #チャンネル名のあるjsonファイルを選択
        for file in glob.glob(import_path + "/" + channel_name + "*.csv"):
            df = pd.read_csv(file)

            #"day"でソート
            df = df.sort_values("day")
            
            #1日の差分を求める
            df_diff = df.diff()
            
            #データが列方向1つ下にズレているので修正(列方向上に1つだけシフトする)
            df_diff = df_diff.shift(periods=-1)
            
            #新しい列を追加
            df["viewCount_diff"] = df_diff["viewCount"]
            df["subscriberCount_diff"] = df_diff["subscriberCount"]
            df["videoCount_diff"] = df_diff["videoCount"]
            df["channel_num"] = channel_counter
            
            
            
            #欠損値がある行を削除
            df = df.dropna(axis=0)
            
            df_all = pd.concat([df_all, df])


        channel_counter += 1 


        
        #チャンネルごとの差分データベースを保存する場合はこっちを使う
        # df.to_csv(OUTPUT_PATH + "/" + channel_name + "_diff.csv", index=False)
        
    df_all["channel_num"] = df_all["channel_num"].astype(int)
    df_all.to_csv(output_path + "/all_channel_diff.csv", index=False) 



if __name__ == "__main__":
    create_csv(DATA_PATH, DATABASE_PATH)
    create_database(DATABASE_PATH, DATABASE_PATH)