import time, schedule, datetime
from channel_api import YTstat
import read_data

API_KEY = ''

def job(api_key):
    """_summary_
        チャンネルデータを取得
    Args:
        api_key : YouTube data api を使用するためのAPIKEY
    """
    #テキストファイルにあるチャンネルIDとチャンネル名のデータを取得
    channel_ids = read_data.get_channel_data()
    
    
    #データ取得
    for channel_id in channel_ids:
        yt = YTstat(api_key, channel_id[0], channel_id[1])
        yt.get_channel_statistics()
        yt.dump()
        
        
    s = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print("I'm working..." + s)



if __name__ == "__main__":
    schedule.every().day.at("00:00").do(job, API_KEY)
    while True:
        schedule.run_pending()
        time.sleep(1)
